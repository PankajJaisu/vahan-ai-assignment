from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ResearchPaper
from .serializers import ResearchPaperSerializer
from .agents.extraction_agent import ExtractionAgent
from .agents.summary_agent import SummaryAgent
from .agents.audio_agent import AudioAgent
from .agents.topic_classifier_agent import TopicClassificationAgent
from .agents.paper_search_agent import PaperSearchAgent
import os
import uuid
import requests
from bs4 import BeautifulSoup

class SearchAndClassifyView(APIView):
    def get(self, request):
        topic_query = request.GET.get("topic")
        candidate_topics = ["Artificial Intelligence", "Quantum Computing", "Healthcare", "Finance", "Climate Change"]

        if not topic_query:
            return Response({"error": "Topic query is required."}, status=400)

        search_agent = PaperSearchAgent()
        classifier = TopicClassificationAgent()
        summarizer = SummaryAgent()
        audio_agent = AudioAgent()

        results = search_agent.search_arxiv(topic_query)
        saved = []

        for paper in results:
            best_topic = classifier.classify(paper["summary"], candidate_topics)
            summary = summarizer.summarize(paper["summary"])

            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join("media/audios", audio_filename)
            audio_agent.generate_audio(summary, audio_path, best_topic)

            saved_paper = ResearchPaper.objects.create(
                title=paper["title"],
                summary=summary,
                topic=best_topic,
                source_url=paper["link"],
                audio=f"audios/{audio_filename}"
            )
            saved.append(ResearchPaperSerializer(saved_paper).data)

        return Response(saved)

    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        extraction_agent = ExtractionAgent()
        extracted_text = extraction_agent.extract_from_url(url)

        if not extracted_text:
            return Response({'error': 'Could not extract text from URL'}, status=status.HTTP_400_BAD_REQUEST)

        classifier_agent = TopicClassificationAgent()
        labels = ["Artificial Intelligence", "Quantum Computing", "Healthcare", "Finance", "Climate Change"]
        topic = classifier_agent.classify(extracted_text[:500], labels)

        summary_agent = SummaryAgent()
        summary = summary_agent.summarize(extracted_text)

        audio_agent = AudioAgent()
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join('media/audios/', audio_filename)
        audio_agent.generate_audio(summary, audio_path, topic)

        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1].replace("-", " ").replace(".pdf", "").title()

        paper = ResearchPaper.objects.create(
            title=title,
            topic=topic,
            summary=summary,
            source_url=url,
            audio=f"audios/{audio_filename}"
        )
        serializer = ResearchPaperSerializer(paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProcessDOIView(APIView):
    def post(self, request):
        doi = request.data.get('doi')
        if not doi:
            return Response({'error': 'DOI is required'}, status=status.HTTP_400_BAD_REQUEST)

        extraction_agent = ExtractionAgent()
        extracted_text = extraction_agent.extract_from_doi(doi)

        if not extracted_text:
            return Response({'error': 'Could not extract text from DOI'}, status=status.HTTP_400_BAD_REQUEST)

        classifier_agent = TopicClassificationAgent()
        labels = ["Artificial Intelligence", "Quantum Computing", "Healthcare", "Finance", "Climate Change"]
        topic = classifier_agent.classify(extracted_text[:500], labels)

        summary_agent = SummaryAgent()
        summary = summary_agent.summarize(extracted_text)

        audio_agent = AudioAgent()
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join('media/audios/', audio_filename)
        audio_agent.generate_audio(summary, audio_path, topic)

        html = requests.get(f"https://doi.org/{doi}", timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else doi.replace("/", " ").replace("-", " ").title()

        paper = ResearchPaper.objects.create(
            title=title,
            doi=doi,
            topic=topic,
            summary=summary,
            audio=f"audios/{audio_filename}"
        )
        serializer = ResearchPaperSerializer(paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UploadPaperView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        temp_path = f"/tmp/{uuid.uuid4()}_{file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        extraction_agent = ExtractionAgent()
        extracted_text = extraction_agent.extract_text(temp_path)
        os.remove(temp_path)

        if not extracted_text:
            return Response({'error': 'Failed to extract text from PDF'}, status=status.HTTP_400_BAD_REQUEST)

        classifier_agent = TopicClassificationAgent()
        labels = ["Artificial Intelligence", "Quantum Computing", "Healthcare", "Finance", "Climate Change"]
        topic = classifier_agent.classify(extracted_text[:500], labels)

        summary_agent = SummaryAgent()
        summary = summary_agent.summarize(extracted_text)

        audio_agent = AudioAgent()
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join('media/audios/', audio_filename)
        audio_agent.generate_audio(summary, audio_path, topic)

        # Try extracting metadata title from PDF
        try:
            with fitz.open(temp_path) as doc:
                title = doc.metadata.get("title") or file.name.replace('.pdf', '').replace('_', ' ').title()
        except Exception:
            title = file.name.replace('.pdf', '').replace('_', ' ').title()

        paper = ResearchPaper.objects.create(
            title=title,
            topic=topic,
            summary=summary,
            file=file,
            audio=f"audios/{audio_filename}"
        )
        serializer = ResearchPaperSerializer(paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProcessAcademicRepoURLView(APIView):
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL is required"}, status=400)

        try:
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, 'html.parser')

            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1].replace("-", " ").replace(".html", "").title()

            article = soup.find("article")
            paragraphs = article.find_all("p") if article else soup.find_all("p")

            text_blocks = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
            if not text_blocks:
                divs = soup.find_all("div")
                text_blocks = [div.get_text(strip=True) for div in divs if len(div.get_text(strip=True)) > 50]

            extracted_text = " ".join(text_blocks)

        except Exception as e:
            return Response({"error": "Failed to extract from academic repository", "details": str(e)}, status=500)

        if not extracted_text.strip():
            return Response({"error": "No meaningful content found at URL"}, status=400)

        classifier_agent = TopicClassificationAgent()
        labels = ["Artificial Intelligence", "Quantum Computing", "Healthcare", "Finance", "Climate Change"]
        topic = classifier_agent.classify(extracted_text[:500], labels)

        summary_agent = SummaryAgent()
        summary = summary_agent.summarize(extracted_text)

        audio_agent = AudioAgent()
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join('media/audios/', audio_filename)
        audio_agent.generate_audio(summary, audio_path, topic)

        paper = ResearchPaper.objects.create(
            title=title,
            topic=topic,
            summary=summary,
            source_url=url,
            audio=f"audios/{audio_filename}"
        )
        serializer = ResearchPaperSerializer(paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ResearchPaperListView(APIView):
    def get(self, request):
        papers = ResearchPaper.objects.all()
        serializer = ResearchPaperSerializer(papers, many=True)
        return Response(serializer.data)

class ResearchPaperDetailView(APIView):
    def get(self, request, pk):
        try:
            paper = ResearchPaper.objects.get(pk=pk)
        except ResearchPaper.DoesNotExist:
            return Response({'error': 'Paper not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResearchPaperSerializer(paper)
        return Response(serializer.data)

class SynthesizeSummaryView(APIView):
    def get(self, request):
        topic = request.GET.get("topic")
        if not topic:
            return Response({"error": "Topic is required"}, status=400)

        papers = ResearchPaper.objects.filter(topic=topic)
        combined_summary = " ".join(p.summary for p in papers if p.summary)

        if not combined_summary:
            return Response({"error": "No summaries found for this topic"}, status=404)

        summary_agent = SummaryAgent()
        synthesized_summary = summary_agent.summarize(combined_summary)
        return Response({"topic": topic, "synthesized_summary": synthesized_summary})


