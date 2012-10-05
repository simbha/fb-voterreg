from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date, datetime
from django.utils import timezone

WONT_VOTE_REASONS = (
    ("not_17", "Won't be 17 yet"),
    ("not_citizen", "Not a citizen"),
    ("dont_want_to", "I don't want to"),
    ("rather_not_say", "I'd rather not say")
)

BATCH_SIZE = 32

BATCH_BARELY_LEGAL = 1
BATCH_FAR_FROM_HOME = 2
BATCH_NEARBY = 3
BATCH_REGULAR = 4
BATCH_RANDOM = 5
BATCH_TYPES = (
    (BATCH_BARELY_LEGAL, "Barely legal"),
    (BATCH_FAR_FROM_HOME, "Far from home"),
    (BATCH_NEARBY, "Nearby"),
    (BATCH_REGULAR, "Not pledged yet"),
    (BATCH_RANDOM, "Not pledged yet"))

BATCH_MAP = dict(BATCH_TYPES)

class User(models.Model):
    fb_uid = models.CharField(max_length=32, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, blank=True)
    first_name = models.CharField(max_length=64, blank=True, default="")
    last_name = models.CharField(max_length=64, blank=True, default="")
    email = models.CharField(max_length=128, blank=True, default="")
    num_friends = models.IntegerField(null=True)
    birthday = models.DateTimeField(null=True)
    far_from_home = models.BooleanField(default=False)
    location_city = models.CharField(max_length=64, blank=True, default="")
    location_state = models.CharField(max_length=64, blank=True, default="")
    location_name = models.CharField(max_length=128, blank=True, default="")
    registered = models.BooleanField(default=False)
    used_registration_widget = models.BooleanField(default=False)
    wont_vote_reason = models.CharField(
        max_length=18, choices=WONT_VOTE_REASONS, blank=True, default="")
    date_pledged = models.DateTimeField(null=True)
    date_invited_friends = models.DateTimeField(null=True)
    # number of invited friends who have pledged
    invited_pledge_count = models.IntegerField(default=0)
    # have we asked votizen api for my data yet?
    data_fetched = models.BooleanField(default=False)
    votizen_id = models.CharField(max_length=132, blank=True, default="")
    friends_fetch_last_activity = models.DateTimeField(null=True)
    # whether or not the friend fetch completed.
    friends_fetched = models.BooleanField(default=False)
    # unsubscribed from emails?
    unsubscribed = models.BooleanField(default=False)

    def update_friends_fetch(self):
        self.friends_fetch_last_activity = datetime.now()

    def friends_need_fetching(self):
        if self.friends_fetched:
            return False
        if not self.friends_fetch_last_activity:
            return True # process hasn't started yet        
        time_since_last_fetch = \
            datetime.now() - self.friends_fetch_last_activity
        if time_since_last_fetch.days > 0:
            return True
        if time_since_last_fetch.seconds > 30:
            return True
        return False # process is still running.

    @property
    def wont_vote(self):
        return self.wont_vote_reason != ""

    @property
    def pledged(self):
        return self.date_pledged is not None

    @property
    def invited_friends(self):
        return self.date_invited_friends is not None

    def is_admirable(self):
        return self.registered or self.pledged or self.invited_friends

class FriendshipBatch(models.Model):
    user = models.ForeignKey(User)
    count = models.IntegerField(default=0)
    regular_batch_no = models.IntegerField(default=1)
    type = models.IntegerField(choices=BATCH_TYPES)
    invite_date = models.DateTimeField(null=True)
    completely_fetched = models.BooleanField(default=False)

    @property
    def friendships(self):
        return self.friendship_set.all()[:BATCH_SIZE]

    @property
    def title(self):
        if self.type == BATCH_NEARBY:
            return "Friends in {0}, {1}".format(
                self.user.location_city, self.user.location_state)
        else:
            return BATCH_MAP[self.type]

    @property
    def city(self):
        return self.user.location_city

    @property
    def short_description(self):
        f = self.friendship_set.all()[:3]
        if self.count == 1:
            return u"{0} is".format(f[0].name)
        elif self.count == 2:
            return u"{0} and {1} are".format(
                f[0].name, f[1].name)
        elif self.count == 3:
            return u"{0}, {1}, and {2} are".format(
                f[0].name, f[1].name, f[2].name)
        else:
            return u"{0}, {1}, and {2} others are".format(
                f[0].name, f[1].name, self.count - 2)

    @property
    def unknown_description(self):
        f = self.friendship_set.all()[:3]
        if self.count == 1:
            return u"{0} is".format(f[0].name)
        elif self.count == 2:
            return u"{0} and {1}".format(
                f[0].name, f[1].name)
        elif self.count == 3:
            return u"{0}, {1}, and {2}".format(
                f[0].name, f[1].name, f[2].name)
        else:
            return u"{0}, {1}, and {2} others".format(
                f[0].name, f[1].name, self.count - 2)


class Friendship(models.Model):
    class Meta:
        unique_together = (("user", "fb_uid",),)
    user = models.ForeignKey(User)
    batch = models.ForeignKey(FriendshipBatch, null=True)
    user_fb_uid = models.CharField(max_length=32, db_index=True)
    fb_uid = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=128)
    is_random = models.BooleanField(default=False)
    # registered * 1 + pledged * 1
    display_ordering = models.IntegerField(default=0, db_index=True)
    birthday = models.DateTimeField(null=True)
    far_from_home = models.BooleanField(default=False)
    location_name = models.CharField(max_length=128, blank=True, default="")
    votizen_id = models.CharField(max_length=132, blank=True)
    registered = models.BooleanField(default=False)
    date_pledged = models.DateTimeField(null=True)
    invited_pledge_count = models.IntegerField(default=0)
    wont_vote_reason = models.CharField(
        max_length=18, choices=WONT_VOTE_REASONS, blank=True)

    def needs_invitation(self):
        touched = self.registered or self.pledged or \
            self.invited_pledge_count > 0 or self.wont_vote_reason
        return not touched

    @property
    def pledged(self):
        return self.date_pledged is not None

    @classmethod
    def create(cls, user, fb_uid, name, **kwargs):
        return Friendship(
            user=user, 
            user_fb_uid=user.fb_uid,
            fb_uid=fb_uid,
            name=name, 
            **kwargs)

    @classmethod
    def create_from(cls, user, friend):
        f = Friendship.create(user, friend.fb_uid, friend.name)
        f.update_from(friend)
        return f

    @classmethod
    def create_from_fb_profile(cls, user, fb_profile):
        f = Friendship.create(user, fb_profile.uid, fb_profile.name)
        f.birthday = fb_profile.dob
        f.location_name = fb_profile.location or ""
        f.far_from_home = fb_profile.far_from_home()
        return f

    def update_from(self, user):
        self.birthday = user.birthday
        self.location_name = user.location_name
        self.far_from_home = user.far_from_home
        self.votizen_id = user.votizen_id
        self.registered = user.registered
        self.date_pledged = user.date_pledged
        self.invited_pledge_count = user.invited_pledge_count
        self.wont_vote_reason = user.wont_vote_reason

    def picture_url(self):
        return "https://graph.facebook.com/{0}/picture?type=large".format(
            self.fb_uid)

def _fill_in_display_ordering(sender, instance, **kwargs):
    instance.display_ordering = \
        (1 if instance.registered else 0) + \
        (1 if instance.pledged else 0)
    if not instance.registered and not instance.batch:
        today = date.today()
        user = instance.user
        batch_type = None
        if instance.is_random:
            batch_type = BATCH_RANDOM
        elif instance.birthday and today.year - instance.birthday.year < 22:
            batch_type = BATCH_BARELY_LEGAL
        elif instance.far_from_home:
            batch_type = BATCH_FAR_FROM_HOME
        elif instance.location_name and \
                instance.location_name == user.location_name:
            batch_type = BATCH_NEARBY
        else:
            batch_type = BATCH_REGULAR
        batch, created = FriendshipBatch.objects.get_or_create(
            user=user,
            type=batch_type,
            completely_fetched=False)
        instance.batch = batch

def _update_batch(sender, instance, **kwargs):
    if not instance.batch:
        return
    batch = instance.batch
    batch.count = Friendship.objects.filter(batch=batch).count()
    if batch.count >= BATCH_SIZE:
        batch.completely_fetched = True
        batch.regular_batch_no = FriendshipBatch.objects.filter(
            user=batch.user, type=batch.type).count()
    batch.save()

pre_save.connect(_fill_in_display_ordering, sender=Friendship, 
                 dispatch_uid="fill_in_display_ordering")

post_save.connect(_update_batch, sender=Friendship,
                  dispatch_uid="update_batch")
