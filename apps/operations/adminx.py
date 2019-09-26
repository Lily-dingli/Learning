#-*-coding:utf-8-*-
import xadmin
from apps.operations.models import UserAsk,CourseComments,UserCourse,UserFavorite,UserMessage
class GlobalSettings(object):
    site_title='学霸成长计划后台管理系统'
    site_footer='学霸成长计划'
    # menu_style='accordion'
class BaseSettings(object):
    enable_themes=True
    use_bootswatch=True
class UserAskAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
class UserCourseAdmin(object):
    list_display = ['course', 'user','add_time']
    search_fields = ['course', 'user']
    list_filter = ['course', 'user', 'add_time']
class CourseCommentsAdmin(object):
    list_display = ['course', 'user', 'comments', 'add_time']
    search_fields = ['course', 'user', 'comments']
    list_filter = ['course', 'user', 'comments', 'add_time']
class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type' ,'add_time']
class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSettings)