from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import ResearchPaper
from .serializers import ResearchPaperSerializer
from .agents.extraction_agent import ExtractionAgent
from .agents.summary_agent import SummaryAgent
from .agents.audio_agent import AudioAgent
from .agents.paper_search_agent import PaperSearchAgent
from .agents.topic_classifier_agent import TopicClassificationAgent

class UploadPaperView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ResearchPaperSerializer(data=request.data)
        if serializer.is_valid():
            paper = serializer.save()

            text = ExtractionAgent().extract_text(paper.file.path)
            summary = SummaryAgent().summarize(text)
            audio_path = f"media/audios/{paper.id}.mp3"
            AudioAgent().generate_audio(summary, audio_path)

            paper.summary = summary
            paper.audio = audio_path.replace("media/", "")
            paper.save()

            return Response(ResearchPaperSerializer(paper).data)
        return Response(serializer.errors, status=400)

class ProcessURLPaperView(APIView):
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        text = ExtractionAgent().extract_from_url(url)
        if not text.strip():
            return JsonResponse({"error": "Failed to extract text from URL"}, status=400)

        summary = SummaryAgent().summarize(text)
        topic = TopicClassificationAgent().classify(summary, ["AI", "Quantum Computing", "Climate", "Biology", "Medicine"])

        paper = ResearchPaper.objects.create(
            title="From URL",
            summary=summary,
            topic=topic,
            source_url=url,
            citation=f"Paper from {url}"
        )

        audio_path = f"media/audios/{paper.id}.mp3"
        AudioAgent().generate_audio(summary, audio_path)
        paper.audio = audio_path.replace("media/", "")
        paper.save()

        return JsonResponse(ResearchPaperSerializer(paper).data)


class ProcessDOIView(APIView):
    def post(self, request):
        doi = request.data.get("doi")
        if not doi:
            return JsonResponse({"error": "DOI is required"}, status=400)

        text = ExtractionAgent().extract_from_doi(doi)
        if not text.strip():
            return JsonResponse({"error": "Failed to extract text from DOI"}, status=400)

        summary = SummaryAgent().summarize(text)
        topic = TopicClassificationAgent().classify(summary, ["AI", "Quantum Computing", "Climate", "Biology", "Medicine"])

        paper = ResearchPaper.objects.create(
            title="From DOI",
            summary=summary,
            topic=topic,
            doi=doi,
            citation=f"Paper from DOI: {doi}"
        )

        audio_path = f"media/audios/{paper.id}.mp3"
        AudioAgent().generate_audio(summary, audio_path)
        paper.audio = audio_path.replace("media/", "")
        paper.save()

        return JsonResponse(ResearchPaperSerializer(paper).data)

class SearchAndClassifyView(APIView):
    def get(self, request):
        topic_query = request.GET.get("topic")

        # Predefined candidate topics used for zero-shot classification. This list can be extended
        # or fetched dynamically in future for improved flexibility.
        candidate_topics = ["AI", "Quantum Computing", "Climate", "Biology", "Medicine"]

        if not topic_query:
            return JsonResponse({"error": "Topic query is required."}, status=400)

        search_agent = PaperSearchAgent()
        classifier = TopicClassificationAgent()

        results = search_agent.search_arxiv(topic_query)
        saved = []

        for paper in results:
            best_topic = classifier.classify(paper["summary"], candidate_topics)

            saved_paper = ResearchPaper.objects.create(
                title=paper["title"],
                summary=paper["summary"],
                topic=best_topic,
                source_url=paper["link"],
                citation=paper["citation"]
            )
            saved.append(ResearchPaperSerializer(saved_paper).data)

        return JsonResponse(saved, safe=False)
