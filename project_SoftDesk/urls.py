"""project_SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tickets_app.api_views import (
    # UserApiView,
    ProjectsViewset,
    # IssuesViewset,
    UserViewSet,
    contributors,
    ContributorDelete,
    GetPostIssues,
    UpdateDeleteIssues,
    CommentListCreate,
    CommentRetrieveUpdateDestroy,
)

# Explicit actions for custom routes
signup = UserViewSet.as_view({
    'post': 'create',
})

get_contributors = ProjectsViewset.as_view({
    'get': 'get_contributors',
})

# router and ViewSets routes
router = SimpleRouter()
router.register(
    prefix='projects', viewset=ProjectsViewset, basename='projects'),
# router.register('tickets', IssuesViewset, 'tickets'),
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # obtain a token pair (authentication):
    path(
        'api/login/', TokenObtainPairView.as_view(), name="login"),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(),
        name="token_refresh"),
    # custom routes to explicitely defined actions:
    path('api/signup/', signup, name='signup'),
    path(
        'api/projects/<int:project_id>/users/',
        contributors, name='contributors'),
    path(
        'api/projects/<int:project_id>/users/<int:user_id>/',
        ContributorDelete.as_view(), name='contributor_delete'),
    path(
        'api/projects/<int:project_id>/issues/',
        GetPostIssues.as_view(), name="get_post_issues"
    ),
    path(
        'api/projects/<int:project_id>/issues/<int:issue_id>',
        UpdateDeleteIssues.as_view(), name="update_delete_issues"
    ),
    path(
        'api/projects/<int:project_id>/issues/<int:issue_id>/comments/',
        CommentListCreate.as_view(), name="comment_list_create"
    ),
    path(
        (
            'api/projects/<int:project_id>/issues/'
            '<int:issue_id>/comments/<int:comment_id>'
        ),
        CommentRetrieveUpdateDestroy.as_view(),
        name="comment_retrieve_update_destroy"
    ),
]
