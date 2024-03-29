from typing import DefaultDict

from flask.json import jsonify


class elb_class:
    def __init__(self, account_dic, specified_account):
        print("init elb")
        self.description = "elb"
        self.account_name = specified_account
        self.elb_list = []
        self.result = {"state":"lookup all elb in account" , "data": []}
        try:
            # 다중계정
            if specified_account == "All":
                print("All Account")
                for account_name in account_dic:
                    self.elb_list.append({
                        "account_name" : account_name ,
                        "client" : account_dic[account_name].client(
                            service_name='elbv2'
                        ),
                        "ec2_client" : account_dic[account_name].client(
                            service_name='ec2'
                        )  
                    })
            # 단일계정
            else:
                print(specified_account + "Account")
                self.elb = account_dic[specified_account].client(
                    service_name='elbv2'
                )
        except Exception as e:
            print(e)
            print("Wrong Account credentials")

    # elb 조회
    def lookup(self):
        print("Lookup all elb")
        for account_i in range(len(self.elb_list)):
            client = self.elb_list[account_i]["client"]
            ec2_client = self.elb_list[account_i]["ec2_client"]
            print(client)
            elb_response = client.describe_load_balancers()['LoadBalancers']
            for i in range (len(elb_response)):
                lbArn = elb_response[i]["LoadBalancerArn"]
                tgState, tgDic = self.get_target_group_state(client,ec2_client,lbArn)
                type = elb_response[i]["Type"]
                if type =="network" :
                    type = "NLB"
                elif type =="application":
                    type = "ALB"
                elif type =="gateway":
                    type = "GLB"
                else:
                    type = "maybe CLB"
                
                self.result["data"].append({
                    "Account" : self.elb_list[account_i]["account_name"],
                    "Name" : elb_response[i]["LoadBalancerName"],
                    "DNS" : elb_response[i]["DNSName"],
                    "TYPE" : type,
                    "TGState" : tgState,
                    "TGCount": len(tgDic),
                    ## 안보여지는 정보
                    "LoadBalancerArn" : lbArn,
                    "TGDic" : tgDic
                })
        return self.result

    # target group 상태
    def get_target_group_state(self, client,ec2_client, loadBalancerArn ):
        # port 별로 Target Group이 존재
        # ELB - TG  - target instance
        #           - target instance
        #           -  ...
        #     - TG
        #       ...
        
        
        # 특정 lb에서의 Target Group들
        target_groups = client.describe_target_groups(
            LoadBalancerArn = loadBalancerArn,
        )["TargetGroups"]

        target_groups_dic = [0 for _ in range(len(target_groups))]
        target_groups_state = []
        tg_index = 0
        # 특정 LB - Target Group들의 각각의 instance 정보
        for target_group in target_groups:
            targetgroupArn = target_group["TargetGroupArn"]
            targetgroupName = target_group["TargetGroupName"]
            targetgroupPort = target_group["Port"]
            target_groups_dic[tg_index] = {
                "Name": targetgroupName,
                "Arn": targetgroupArn,
                "Port": targetgroupPort,
                "Protocol": target_group["Protocol"],
                "Target_Instance" : []
                }
            
            targets = client.describe_target_health(
                TargetGroupArn = targetgroupArn
            )["TargetHealthDescriptions"]
            target_unhealthy_count = 0
            for target in targets:
                target_state = target["TargetHealth"]["State"]
                target_state_color = "gray"
                if target_state == "unhealthy":
                    target_unhealthy_count += 1
                    target_state_color = "red"
                if target_state == "healthy":
                    target_state_color = "green"
                target_id = target["Target"]["Id"]
                if "i" in target_id:
                    #  target이 인스턴스인 경우
                    target_name_tag = ec2_client.describe_instances(
                        InstanceIds=[
                            target_id
                        ]
                    )["Reservations"][0]["Instances"][0]["Tags"]
                    for i in target_name_tag:
                        if i["Key"] == "Name":
                            target_name = i["Value"]
                else: 
                    # target이 ELB? IP?인경우
                    target_name = target_id

                target_groups_dic[tg_index]["Target_Instance"].append({
                    "Id": target_id,
                    "Name": target_name,
                    "HealthCheckPort0": target["HealthCheckPort"],
                    "State": target_state_color
                })
            target_group_state_color = self.set_state_color(len(targets),target_unhealthy_count)
            target_groups_dic[tg_index]["State"] = target_group_state_color
            target_groups_state.append((target_group_state_color, targetgroupPort))
            tg_index += 1


        return target_groups_state , target_groups_dic

    def set_state_color(self, total_count, unhealth_count):
        if total_count == 0:
            return "gray"
        if unhealth_count == 0:
            return "green"
        elif unhealth_count < total_count:
            return "orange"
        elif unhealth_count == total_count:
            return "red"
        else:
            print("Error : Something Wrong")
            return "Error"

    # 특정 elb 검색
    def search(self,elb_name_list):
        print("Lookup specified elb")
        elb_response2 = self.elb.describe_load_balancers(
            Names = elb_name_list.split(",")
        )
        return elb_response2['LoadBalancers']

    # 특정 elb 변경
    def fix_elb(self,elb_info):
        return

