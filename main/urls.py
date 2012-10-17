from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    "main.views",
    url(r"^$", "index", name="index"),
    url(r"^fetch_me$", "fetch_me", name="fetch_me"),
    url(r"^fetch_friends$", "fetch_friends", name="fetch_friends"),
    url(r"^register$", "register", name="register"),
    url(r"^register_widget$", "register_widget", name="register_widget"),
    url(r"^my_vote$", "my_vote", name="my_vote"),
    url(r"^my_vote/register$", "my_vote_register", name="my_vote_register"),
    url(r"^my_vote/pledge$", "my_vote_pledge", name="my_vote_pledge"),
    url(r"^my_vote/vote$", "my_vote_vote", name="my_vote_vote"),
    url(r"^pledge$", "pledge", name="pledge"),
    url(r"^unpledge$", "_unpledge", name="unpledge"),
    url(r"^submit_pledge$", "submit_pledge", name="submit_pledge"),
    url(r"^actually_registered$", "im_actually_registered", name="actually_registered"),
    url(r"^wont_vote$", "wont_vote", name="wont_vote"),
    url(r"^missions$", "missions", name="missions"),
    url(r"^fetch_updated_batches$", "fetch_updated_batches", name="fetch_updated_batches"),
    url(r"^mark_batch_invited$", "mark_batch_invited", name="mark_batch_invited"),
    url(r"^mark_individual_invited$", "mark_individual_invited", name="mark_individual_invited"),
    url(r"^single_user_invited$", "single_user_invited", name="single_user_invited"),
    url(r"^friends_list$", "friends_list"),
    url(r"^unsubscribe", "unsubscribe", name="unsubscribe"),
    url(r"^invite_friends_2$", "invite_friends_2", name="invite_friends_2"),
    url(r"^invite_friends_2/(?P<section>\w+)$", "invite_friends_2", name="invite_friends_2"),
    url(r"^invite_friends_2_page/(?P<section>\w+)$", "invite_friends_2_page", name="invite_friends_2_page"),
    url(r"^mission$", "mission", name="mission"),
    url(r"^mission/(?P<batch_type>\d+)", "mission", name="mission"),
    url(r"^mission_friends_page/(?P<batch_type>\d+)", "mission_friends_page", name="mission_friends_page"),
    url(r"^mark_mission_batch_invited/(?P<batch_type>\d+)", "mark_mission_batch_invited", name="mark_mission_batch_invited"),
)

urlpatterns += patterns(
    "",
    url(r"^voterreg_invite$",
        TemplateView.as_view(template_name="voterreg_invite.html"),
        name="voterreg_invite"),
    url(r"^no_cookies$",
        TemplateView.as_view(template_name="no_cookies.html"),
        name="no_cookies"),
)
