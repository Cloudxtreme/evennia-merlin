from django.db import models

"""
Misc. utility methods. Keep these to a minimum.
"""

def myrddin_date_format(dtime):
    """
    Myrddin used the format, 'Mon Jan 01', for showing dates. Output
    the given datetime object in this format.
    
    :param datetime.datetime dtime: The datetime object to print out.
    :rtype: str
    :returns: A Myrddin-style date string for last post date.
    """
    return dtime.strftime('%a %b %d')

"""
Models and managers.
"""

class BBGroupManager(models.Manager):
    """
    Convenience table-level methods for BB groups. Logic for filtering based
    on subscriptions should stay here, along with any other commonly used
    filtering.
    """
    def get_groups_for_player(self, player):
        """
        :param PlayerDB player: The player whose BB group list to retrieve.
        """
        return self.all()

class BBGroup(models.Model):
    """
    This is what Myrddin called boards or forums. It represents one chunk
    of the BBS, and contains BBPost objects. De-norm things on to this model
    where it will help us with frequently used commands.
    """
    name = models.CharField(max_length=255)
    last_post_dtime = models.DateTimeField(blank=True, null=True)
    num_posts = models.PositiveIntegerField(default=0)

    objects = BBGroupManager()

    def get_last_post_dtime_display_str(self):
        """
        Myrddin used the format, 'Mon Jan 01', for showing dates. Output
        the last posted date in this format.
        
        :rtype: str
        :returns: A Myrddin-style date string for last post date.
        """
        if not self.last_post_dtime:
            return "Never"
        else:
            return myrddin_date_format(last_post_dtime)

    class Meta:
        ordering = ['id']

class BBPost(models.Model):
    """
    An individual BB post. Owned by a player, held within a BBGroup.
    """
    group = models.ForeignKey(BBGroup)
    author = models.ForeignKey('players.PlayerDB')
    title = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        ordering = ['id']
