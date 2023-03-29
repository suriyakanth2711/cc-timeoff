from urllib import response
import requests
from rest_framework.response import Response
from rest_framework import status, generics
from timeoff_api.models import  PolicyModel, LeaveModel
from timeoff_api.serializers import  PolicySerializer, LeaveSerializer
from datetime import datetime


class Policies(generics.GenericAPIView):
    serializer_class = PolicySerializer
    queryset = PolicyModel.objects.all()
    def get(self, request, org):
        policies = PolicyModel.objects.filter(organization = org)
        serializer = self.serializer_class(policies, many=True)
        return Response(serializer.data)





class Policy(generics.GenericAPIView):
    serializer_class = PolicySerializer
    queryset = PolicyModel.objects.all()
    def get_policy(self,pk):
        try:
            return PolicyModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, org, pk):
        print(pk)
        if isinstance(pk, int):
            policies = PolicyModel.objects.filter(id = pk)
            serializer = self.serializer_class(policies, many=True)
            return Response(serializer.data)
        else :
            return Response([])

    def post(self, request, org, pk):
        if pk=='new':
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "policy": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "fail", "message": "Invalid endpoint"}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, org, pk):
        policy = self.get_policy(pk)
        if policy == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(policy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['last_udpated_on'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "policy": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, org, pk):
        policy = self.get_policy(pk)
        if policy == None:
            return Response({"status": "fail", "message": f"policy with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Leave(generics.GenericAPIView):
    serializer_class = LeaveSerializer
    policies = PolicyModel.objects.all()
    queryset = LeaveModel.objects.all()

    def get_leave(self,pk):
        try:
            return LeaveModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, org, eid):
        leaves = LeaveModel.objects.filter(employee_ID = eid)
        serializer = self.serializer_class(leaves, many=True)
        leaves_with_types = {}
        for leave in serializer.data:
            if leave['leave_type'] not in leaves_with_types.keys():
                todt = lambda x : (datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ'))
                leaves_with_types[leave['leave_type']] = (todt(leave['end_date']) - todt(leave['start_date'])).days
            else:
                leaves_with_types[leave['leave_type']] += (todt(leave['end_date']) - todt(leave['start_date'])).days

        
        employee_details = requests.post(url = "https://employee-data-platform.vercel.app/api/fetchone", json = {"id":eid})
        
        
        if employee_details.json() == []:
            return Response({"status": "fail", "message": "Employee ID not found."}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            x = employee_details.json()[0]
            employee = {"designation":x["employee_role"], "first_name":x["first_name"], "last_name":x["last_name"]}

        allowed_leaves = {}
        policies = self.policies.filter(designation=employee["designation"],organization = org)
        for policy in PolicySerializer(policies,many=True).data:
            allowed_leaves[policy['leave_type']] = policy['num_of_leaves']
        
        response = {"name":employee,"taken_leaves": leaves_with_types, "available_leaves":allowed_leaves,"leaves_list":serializer.data}

        return Response(response)

    def post(self, request, org ,eid):
        data = request.data.copy()
        data['employee_ID'] = eid
        if data["status"] =="" :
            data["status"] = "approved"
           # data = {**request.data, "status": "approved"}
        if data['start_date'] >= data['end_date']:
            return Response({"status": "fail", "message": "Invalid Date Range Selected"}, status=status.HTTP_400_BAD_REQUEST)

        employee_details = requests.post(url = "https://employee-data-platform.vercel.app/api/fetchone", json = {"id":eid})
        if employee_details.json() == []:
            return Response({"status": "fail", "message": "Employee ID not found."}, status=status.HTTP_400_BAD_REQUEST)
        employee = {"designation":employee_details.json()[0]["employee_role"]}

        policy = self.policies.filter(leave_type = data['leave_type'], designation=employee["designation"],organization = org)
        policy_data = PolicySerializer(policy,many=True).data[0]
        todt = lambda x : (datetime.strptime(x,'%Y-%m-%dT%H:%M'))

        #number of days
        duration = (todt(data['end_date']) - todt(data['start_date'])).days

        #Existing leave
        leaves = LeaveModel.objects.filter(employee_ID = data['employee_ID'], leave_type = data['leave_type'])
        print(leaves)
        serializer = self.serializer_class(leaves,many=True)
        existing_leaves = 0
        for leave in serializer.data:
            todt = lambda x : (datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ'))
            existing_leaves += (todt(leave['end_date']) - todt(leave['start_date'])).days

        if existing_leaves + duration > policy_data['num_of_leaves']:
            return Response({"status": "fail", "message": "Number of leaves exceeding limit"}, status=status.HTTP_400_BAD_REQUEST)

        #continous leaves
        if duration > policy_data['max_num_cont_leaves']:
            ## Needs to be fixed. checks for only one leave
            ## if a person applies 2 seperate leaves in continous dates, it can exceed the limit.
            ## need to check all leaves
            return Response({"status": "fail", "message": "Number of continous leaves exceeding limit"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "policy": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

