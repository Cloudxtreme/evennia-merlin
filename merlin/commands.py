from src.commands.cmdset import CmdSet
from game.gamesrc.commands.basecommand import MuxCommand
from merlin.models import BBGroup

def ordered_num_to_group(ordered_num):
    """
    The users refer to BB groups by the order in which they appear in the
    master list of groups. +bblist can be used to see the canonical list
    of groups and their cosmetic IDs.
    
    We call these IDs cosmetic, since they don't in fact match the BBGroup
    object's primary key.
    
    :param int ordered_num: A BB group's "cosmetic" ID. That is, what shows
        up on +bblist and +bbread. This number is the group's order within
        the default QuerySet.
    :rtype: BBGroup
    :returns: The appropriate BBGroup, based on the cosmetic ID.
    :raises: ValueError, IndexError
    """
    group_num = int(ordered_num)
    return BBGroup.objects.all()[group_num - 1]

class CmdBbRead(MuxCommand):
    """
    TODO: Docs
    """
    key = "+bbread"
    help_category = "BBS"

    def func(self):
        caller = self.caller

        if not self.args:
            # Render the default BB group index.
            self.emit_index()

    def emit_index(self):
        """
        No args provided, show the BB group index.
        """
        caller = self.caller
        buffer = "=" * 78 + "\n"
        buffer += "%s %s %s\n" % (
                      'Group Name'.rjust(17).ljust(40),
                      'Last Post'.ljust(15),
                      '# of messages',
                  )
        buffer += "-" * 78 + "\n"

        groups = BBGroup.objects.get_groups_for_player(None)
        group_counter = 1
        for group in groups:
            # XXX: Sub values.
            buffer += " %s %s %s %s %s\n" % (
                          str(group_counter).ljust(5),
                          group.name.ljust(33),
                          group.get_last_post_dtime_display_str().ljust(15),
                          str(group.num_posts).rjust(7),
                          'U',
                      )
            group_counter += 1

        buffer += "-" * 78 + "\n"
        buffer += "'*' = restricted     '-' = read only     '(-)' = read only, but you can write\n"
        buffer += "=" * 78 + "\n"
        caller.msg(buffer)

class CmdBbNewGroup(MuxCommand):
    """
    TODO: Docs
    """
    key = "+bbnewgroup"
    help_category = "BBS"

    def func(self):
        "This actually does things"
        caller = self.caller
        # we don't add any more functionality in this example
        caller.msg("Args: %s" % self.args)

        if not self.args:
            caller.msg("You must specify a new group name.")

        group_name = ''.join(self.args).strip()[:255]
        group = BBGroup.objects.create(name=group_name)
        caller.msg("You have created a new BB group: %s" % group_name)

class CmdBbClearGroup(MuxCommand):
    """
    TODO: Docs
    """
    key = "+bbcleargroup"
    help_category = "BBS"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("You must specify the group number to clear (as per +bblist).")

        try:
            group = ordered_num_to_group(self.args[0])
        except ValueError:
            # Probably not an int.
            caller.msg("Invalid BB group ID specified.")
            return
        except BBGroup.DoesNotExist:
            caller.msg("No such BB group can be found. See +bblist for a full list.")
            return

        caller.msg("You have deleted the BB group: %s" % group.name)
        group.delete()

class CmdBbList(MuxCommand):
    """
    TODO: Docs
    """
    key = "+bblist"
    help_category = "BBS"

    def func(self):
        caller = self.caller
        buffer = "=" * 78 + "\n"
        # XXX: Use string formatting here.
        buffer += "Available Bulletin Board Groups      Member?        Timeout (in days)\n"
        buffer += "-" * 78 + "\n"

        group_counter = 1
        for group in BBGroup.objects.all():
            buffer += " %4d  %s %s %s\n" % (
                          group_counter,
                          group.name.ljust(30),
                          'Yes'.ljust(17),
                          'NotImpl',
                      )
            group_counter += 1

        buffer += "-" * 78 + "\n"
        buffer += "To join groups, type '+bbjoin <group number or name>'\n"
        buffer += "=" * 78 + "\n"
        caller.msg(buffer)

class CmdBbPost(MuxCommand):
    """
    TODO: Docs
    """
    key = "+bbpost"
    help_category = "BBS"

    def func(self):
        caller = self.caller
        caller.msg("Kerpow!")

class MerlinBbCmdSet(CmdSet):
    """
    This gets added to whatever command set you'd like the BB to be accessible
    from. Your default command set is recommended.
    """
    key = "MerlinBbCmdSet"

    def at_cmdset_creation(self):
        self.add(CmdBbClearGroup())
        self.add(CmdBbList())
        self.add(CmdBbNewGroup())
        self.add(CmdBbPost())
        self.add(CmdBbRead()) 