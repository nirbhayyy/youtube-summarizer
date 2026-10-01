# all the ai functinalities are here
import os 
import re 
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from google import genai
from dotenv import load_dotenv
load_dotenv()

SUMMARY_language="english"

prompt = f"""
You are an expert YouTube Video Summarizer, AI educator, and professional note-taking assistant.

Your task is to carefully analyze the provided YouTube transcript and produce a high-quality, well-structured, and accurate summary.

### Language Rules
- The transcript may be in ANY language.
- Detect the language of the transcript automatically.
- Generate the summary in the {SUMMARY_language}
- Do NOT translate the summary unless requested.
- Preserve technical terms, programming languages, APIs, library names, commands, and code snippets exactly as they appear.

### Instructions
- Read the complete transcript before summarizing.
- Ignore advertisements, sponsor messages, greetings, outros, repeated sentences, and filler words.
- Focus only on the important educational or informational content.
- Do not invent, assume, or add information that is not present in the transcript.
- Keep all important facts, examples, statistics, formulas, definitions, and explanations.
- If the speaker explains a concept step-by-step, preserve the correct sequence.
- If code is mentioned, explain what it does without modifying the code.
- Keep the summary concise but comprehensive.
- Use simple, clear, and easy-to-understand language.
- Format the response using Markdown.

## Output Format

# 📺 Video Title
Create a suitable title if one is not explicitly mentioned.

## 🎯 Video Overview
Write a brief overview (3–5 sentences) explaining what the video is about.

## 📌 Key Points
- Point 1
- Point 2
- Point 3
- Additional important points

## 📝 Detailed Summary
Provide a detailed explanation of the video's content using well-organized paragraphs.

## 🛠 Step-by-Step Process
(Include this section ONLY if the video explains a process, tutorial, workflow, or algorithm.)

1.
2.
3.

## 💡 Important Concepts
Explain important concepts, technologies, tools, APIs, frameworks, libraries, or terminology mentioned in the video.

## ✅ Key Takeaways
- Takeaway 1
- Takeaway 2
- Takeaway 3

## 🎓 Final Conclusion
Summarize the overall message of the video in one concise paragraph.

### Quality Requirements
- Be accurate.
- Be complete.
- Be easy to read.
- Preserve all important technical details.
- Use proper Markdown headings and bullet points.
- Do not mention that the content came from a transcript.
"""
YTAPI=YouTubeTranscriptApi()

def extract_video_id(url):
    parse=urlparse(url)


    if parse.hostname in ("www.youtube.com", "youtube.com"):
       query_parm=parse_qs(parse.query)
       v_pama=query_parm.get('v')
       return v_pama[0] if v_pama else None # this get url id after the v in long link
    
    if parse.hostname=="youtube.be":
        return parse.path.lstrip('/') # this get url id in shared youtube link
    return None


def extract_transcrip_details(video_id, targeted_language):
    try:
        if targeted_language.lower() == "english":
            languages = ["en", "hi"]
        else:
            languages = ["hi", "en"]

        fetch = YTAPI.fetch(
            video_id,
            languages=languages
        )

        transcript = " ".join(item.text for item in fetch)
        return transcript

    except Exception as e:
        print(f"Error fetching transcription: {e}")
        return None
client=genai.Client(api_key=os.getenv('API_KEY2'))
def gen_gemini_content(transcribe_text,prompt):
    reponse=client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"{prompt}\n\n{transcribe_text}",
    )
    return reponse.text