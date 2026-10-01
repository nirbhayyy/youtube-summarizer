from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render,redirect
from . serializers import summaryreqserializer
from . utils import gen_gemini_content,extract_transcrip_details,extract_video_id
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Summary
from django.utils import timezone
from .youtube_service import get_video_details
from .prompts import summary_prompt
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .sentiment import summary_sentiments,overall_sentiment
import isodate
from io import BytesIO
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
import os

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.contrib.admin.views.decorators import staff_member_required


from django.contrib import messages

from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
def formatduration(duration):
    td=isodate.parse_duration(duration)
    total=int(td.total_seconds())
    hours=total//3600
    min=(total%3600)//60
    sec=(total%60)
    if hours:
        return f'{hours} :{min:02}:{sec:02}'
    return f"{min}:{sec:02}"

class SummeryView(APIView):
    def get(self,request):
        return Response({
            "message":"Please POST a youtube_link to this endpoint."}, status=status.HTTP_200_OK)
        
    def post(self,request):
        serializer=summaryreqserializer(data=request.data)
        if serializer.is_valid():
            yt_url=serializer.validated_data['yt_link']
            summary_type=serializer.validated_data['summary_type']
            targeted_language=serializer.validated_data.get('language','english')
            video_id=extract_video_id(yt_url)
            thumbnail_url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            print(targeted_language)

            try:
                transcript_text=extract_transcrip_details(video_id,targeted_language)
                if not transcript_text:
                    return Response({"error":"Transcript not available for this video."}, status=status.HTTP_404_NOT_FOUND)
                Select_prompt_template=summary_prompt.get(summary_type,summary_prompt['standard'])
                if '{summary_language}' in Select_prompt_template:
                    final_prompt=Select_prompt_template.format(summary_language=targeted_language)
                else:
                    final_prompt=Select_prompt_template
             
                summary=gen_gemini_content(transcript_text,final_prompt)
                overall_result=overall_sentiment(transcript_text)
                sentence_result=summary_sentiments(summary)
                details=get_video_details(video_id)
                if details is None:
                    return Response(
                        {'error':'could not fetch the video details'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                saved_summry=Summary.objects.create(
                user=request.user,

                video_title=details["title"],

                youtube_url=yt_url,

                video_id=video_id,

                thumbnail_url=details["thumbnail"],

                channel_name=details["channel"],

                views=int(details["views"]),

                likes=int(details["likes"]),

                duration=formatduration(details["duration"]),   # Format it later if you want

                Summary=summary,

                Summary_language=targeted_language,

                sentiment=overall_result["sentiment"],
                positive_score=overall_result["positive"],
                neutral_score=overall_result["neutral"],
                negative_score=overall_result["negative"],
                compound_score=overall_result["compound"],
        )
                return Response(
                    {
        "id":saved_summry.id,                  
        "video_id": video_id,
        "summary_type": summary_type,
        "thumbnail_url": thumbnail_url,
        "summary": str(summary),
        "sentiment": overall_result["sentiment"],
        'overall_result':overall_result,
        'sentence_result':sentence_result
                 
                        
                    },status=status.HTTP_200_OK
                )
            
            except Exception as e:
                print(f'{e}')
                return Response({"error":f" {e} "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    

def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)

        if form.is_valid():

            user=User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            login(request,user)
            return redirect("login")
    else:
        form=RegisterForm()
    return render(request, "register.html",{'form':form})

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,
                          username=username,
                          password=password)
        if user is not None:
            login(request,user)
            return redirect('summizeui') 
        return render(request,
                      'login.html',
                      {'error':'invalid username or password'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required()
def summary(request):
    return render(request,'index.html')


@login_required()
def dashboard_view(request):
    summries=Summary.objects.filter(user=request.user).order_by('-created_at')
    total_summary=summries.count()
    todays_summary=summries.filter(
        created_at__date=timezone.now().date()
    ).count()

    context={
        'summaries':summries[:],
        'total_summary' : total_summary,
        'todays_summary':todays_summary,
        'channel_name': Summary.channel_name,
        'view':Summary.views,
        'duration':Summary.duration,
        'likes': Summary.likes
        
        
    }

    return render(request,
                  'dashboard.html',
                  context)
class summary_delete(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,summary_id):
        summary=get_object_or_404(Summary,
                                  id=summary_id,
                                  user=request.user)
        summary.delete()

        return Response(
            {"message": "Summary deleted successfully."},status=status.HTTP_200_OK
        )



def homeView(request):
        return render(request,'home.html')

def ExportAsPdf(request, pk):

    summary = get_object_or_404(Summary, pk=pk)

    # Register Unicode font
    font_path = os.path.join(settings.BASE_DIR, "fonts", "DejaVuSans copy.ttf")
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    title_style = ParagraphStyle(
        "Title",
        fontName="DejaVu",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "Heading",
        fontName="DejaVu",
        fontSize=14,
        leading=18,
        spaceAfter=10,
    )

    body_style = ParagraphStyle(
        "Body",
        fontName="DejaVu",
        fontSize=11,
        leading=18,
    )

    story = []

    # Title
    story.append(
        Paragraph("YouTube Video Summary", title_style)
    )

    story.append(Spacer(1, 15))

    # Video title
    story.append(
        Paragraph(
            f"<b>Video Title:</b> {summary.video_title}",
            heading_style
        )
    )

    story.append(Spacer(1, 10))

    # Clean summary text
    text = summary.Summary

    # Remove emojis only
    text = re.sub(
        r"[\U00010000-\U0010ffff]",
        "",
        text
    )

    # Replace markdown line breaks
    text = text.replace("\n", "<br/>")

    story.append(
        Paragraph(text, body_style)
    )

    doc.build(story)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="summary.pdf"
    )


@staff_member_required
def adminView(request):

    # --- Handle admin actions (POST) ---
    if request.method == 'POST':
        action = request.POST.get('action')

        # --- User actions ---
        if action == 'delete_user':
            user_id = request.POST.get('user_id')
            target_user = get_object_or_404(User, id=user_id)

            if target_user == request.user:
                messages.error(request, "You can't delete your own account.")
            elif target_user.is_superuser:
                messages.error(request, "Superuser accounts can't be deleted here.")
            else:
                username = target_user.username
                target_user.delete()
                messages.success(request, f"User '{username}' was deleted.")

            return redirect('admin')

        elif action == 'toggle_active':
            user_id = request.POST.get('user_id')
            target_user = get_object_or_404(User, id=user_id)

            if target_user == request.user:
                messages.error(request, "You can't deactivate your own account.")
            else:
                target_user.is_active = not target_user.is_active
                target_user.save(update_fields=['is_active'])
                state = "activated" if target_user.is_active else "deactivated"
                messages.success(request, f"User '{target_user.username}' was {state}.")

            return redirect('admin')

        elif action == 'toggle_staff':
            user_id = request.POST.get('user_id')
            target_user = get_object_or_404(User, id=user_id)

            if target_user == request.user:
                messages.error(request, "You can't change your own admin status.")
            else:
                target_user.is_staff = not target_user.is_staff
                target_user.save(update_fields=['is_staff'])
                state = "granted" if target_user.is_staff else "revoked"
                messages.success(request, f"Admin access {state} for '{target_user.username}'.")

            return redirect('admin')

        # --- Summary actions ---
        elif action == 'delete_summary':
            summary_id = request.POST.get('summary_id')
            target_summary = get_object_or_404(Summary, id=summary_id)
            title = target_summary.video_title
            target_summary.delete()
            messages.success(request, f"Summary '{title}' was deleted.")
            return redirect('admin')

        elif action == 'update_summary':
            summary_id = request.POST.get('summary_id')
            target_summary = get_object_or_404(Summary, id=summary_id)

            video_title = request.POST.get('video_title', '').strip()
            channel_name = request.POST.get('channel_name', '').strip()
            summary_text = request.POST.get('Summary', '').strip()
            sentiment = request.POST.get('sentiment', '').strip()

            if not video_title or not summary_text:
                messages.error(request, "Video title and summary text can't be empty.")
                return redirect('admin')

            target_summary.video_title = video_title
            target_summary.channel_name = channel_name or target_summary.channel_name
            target_summary.Summary = summary_text

            # Only overwrite sentiment if a valid option was submitted
            if sentiment in ('Positive', 'Negative', 'Neutral'):
                target_summary.sentiment = sentiment

            target_summary.save(update_fields=[
                'video_title', 'channel_name', 'Summary', 'sentiment'
            ])

            messages.success(request, f"Summary '{video_title}' was updated.")
            return redirect('admin')

        else:
            messages.error(request, "Unknown admin action.")
            return redirect('admin')

    # --- GET: build the dashboard, with optional search ---
    user_query = request.GET.get('q_user', '').strip()
    summary_query = request.GET.get('q_summary', '').strip()

    users_qs = User.objects.all().order_by('-date_joined')
    if user_query:
        users_qs = users_qs.filter(
            Q(username__icontains=user_query) | Q(email__icontains=user_query)
        )

    summaries_qs = Summary.objects.select_related('user').order_by('-created_at')
    if summary_query:
        summaries_qs = summaries_qs.filter(
            Q(video_title__icontains=summary_query) |
            Q(channel_name__icontains=summary_query) |
            Q(user__username__icontains=summary_query)
        )
    else:
        summaries_qs = summaries_qs[:20]

    # Paginate users (kept simple — 15 per page)
    user_paginator = Paginator(users_qs, 15)
    user_page = user_paginator.get_page(request.GET.get('user_page'))

    context = {
        'total_users': User.objects.count(),
        'total_summary': Summary.objects.count(),
        'todays_summary': Summary.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'user': user_page,
        'summaries': summaries_qs,
        'user_query': user_query,
        'summary_query': summary_query,
    }

    return render(request, 'admin.html', context)