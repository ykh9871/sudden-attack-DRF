from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.shortcuts import get_object_or_404

from django.db.models import Q, Count
from .models import Group, GroupMember
from user.models import User
from .serializers import (
    GroupSerializer,
    GroupCreateSerializer,
    GroupMembershipRequestSerializer,
    MemberRequestsViewSerializer,
    AdminUserSerializer,
)


class GroupCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(user=request.user)
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = Group.objects.filter(members__user=request.user)
        serializer = GroupSerializer(user_groups, many=True)
        return Response(serializer.data)


class GroupDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        membership = get_object_or_404(GroupMember, group=group, user=request.user)
        if membership.role != "ADMIN":
            return Response(
                {"detail": "Only group admins can delete the group"},
                status=status.HTTP_403_FORBIDDEN,
            )
        group.delete()
        return Response({"message": "Group deleted successfully"})


class GroupJoinRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        GroupMember.objects.create(user=request.user, group=group, role="PENDING")
        return Response({"message": "Successfully send study group join request"})


class MemberRequestsByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = GroupMember.objects.filter(user=request.user, role="PENDING")
        serializer = GroupMembershipRequestSerializer(requests, many=True)
        return Response(serializer.data)


class MemberRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        membership = get_object_or_404(GroupMember, group=group, user=request.user)
        if membership.role != "ADMIN":
            return Response(
                {"detail": "Only group administrators can view member requests."},
                status=status.HTTP_403_FORBIDDEN,
            )
        requests = GroupMember.objects.filter(group=group, role="PENDING")
        serializer = MemberRequestsViewSerializer(requests, many=True)
        return Response(serializer.data)


class MemberAddView(APIView):
    def put(self, request, request_id):
        membership = get_object_or_404(GroupMember, id=request_id)
        membership.role = "MEMBER"
        membership.save()
        return Response({"message": "Successfully added members"})


class MemberDenyView(APIView):
    def delete(self, request, request_id):
        membership = get_object_or_404(GroupMember, id=request_id)
        membership.delete()
        return Response({"message": "Successfully denied request"})


class GroupMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        membership = get_object_or_404(GroupMember, group=group, user=request.user)
        members = GroupMember.objects.filter(group=group).exclude(role="PENDING")
        return Response(
            {
                "current_user_id": request.user.id,
                "role": membership.role,
                "members": [
                    {"id": member.user.id, "nickname": member.user.nickname}
                    for member in members
                ],
            }
        )


class GroupWithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        membership = get_object_or_404(GroupMember, group=group, user=request.user)
        if membership.role == "ADMIN":
            return Response(
                {"detail": "Group administrators are not allowed to leave."},
                status=status.HTTP_403_FORBIDDEN,
            )
        membership.delete()
        return Response({"message": "Successfully left the group."})


class MemberRemoveView(APIView):
    def delete(self, request):
        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            group = get_object_or_404(Group, id=serializer.validated_data["group_id"])
            membership = get_object_or_404(
                GroupMember, group=group, user_id=serializer.validated_data["user_id"]
            )
            if serializer.validated_data["role"] == "ADMIN":
                membership.delete()
                return Response({"message": "Successfully removed a member."})
            else:
                return Response(
                    {"detail": "Only admins can remove members."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupListView(APIView):
    def get(self, request):
        name = request.query_params.get("name")
        groups = Group.objects.annotate(
            member_count=Count("members", filter=~Q(members__role="PENDING"))
        )
        if name:
            groups = groups.filter(name__icontains=name)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class MemberRoleChangeView(APIView):
    def put(self, request, group_id, user_id):
        role = request.data.get("role")
        group = get_object_or_404(Group, id=group_id)
        membership = get_object_or_404(GroupMember, group=group, user_id=user_id)
        if role == "ADMIN":
            if membership.role == "ADMIN":
                return Response({"message": "User's role is already ADMIN"})
            membership.role = "ADMIN"
        elif role == "MEMBER":
            if membership.role == "MEMBER":
                return Response({"message": "User's role is already MEMBER"})
            membership.role = "MEMBER"
        membership.save()
        return Response({"message": "Successfully changed."})
