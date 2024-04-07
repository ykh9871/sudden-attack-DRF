from django.urls import path
from .views import (
    GroupCreateView,
    UserGroupsView,
    GroupDeleteView,
    GroupJoinRequestView,
    MemberRequestsByUserView,
    MemberRequestsView,
    MemberAddView,
    MemberDenyView,
    GroupMembersView,
    GroupWithdrawalView,
    MemberRemoveView,
    GroupListView,
    MemberRoleChangeView,
)

urlpatterns = [
    path("group/", GroupCreateView.as_view(), name="group-create"),
    path("mygroup/", UserGroupsView.as_view(), name="user-groups"),
    path("mygroup/<int:group_id>/", GroupDeleteView.as_view(), name="group-delete"),
    path(
        "member_requests/<int:group_id>/",
        GroupJoinRequestView.as_view(),
        name="group-join-request",
    ),
    path(
        "member_requests/user/",
        MemberRequestsByUserView.as_view(),
        name="member-requests-by-user",
    ),
    path(
        "member_requests/group/<int:group_id>/",
        MemberRequestsView.as_view(),
        name="member-requests",
    ),
    path(
        "member_requests/<int:request_id>/add/",
        MemberAddView.as_view(),
        name="member-add",
    ),
    path(
        "member_requests/<int:request_id>/deny/",
        MemberDenyView.as_view(),
        name="member-deny",
    ),
    path(
        "group/<int:group_id>/members/",
        GroupMembersView.as_view(),
        name="group-members",
    ),
    path(
        "group/<int:group_id>/withdrawal/",
        GroupWithdrawalView.as_view(),
        name="group-withdrawal",
    ),
    path("group/remove_member/", MemberRemoveView.as_view(), name="member-remove"),
    path("group/", GroupListView.as_view(), name="group-list"),
    path(
        "group/<int:group_id>/<int:user_id>/role/",
        MemberRoleChangeView.as_view(),
        name="member-role-change",
    ),
]
