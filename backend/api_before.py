from typing import DefaultDict

from flask.json import jsonify


class elb_class:
    def __init__(self, account_dic, specified_account):
        self.description = "elb"
        self.account_name = specified_account
        self.elb_list = []
        try:
            # 다중계정
            if specified_account == "All":
                print("All Account")
                for account_name in account_dic:
                    self.elb_list.append({
                        "account_name" : account_name ,
                        "client" : account_dic[account_name].client(
                        service_name='elbv2'
                    )})
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
        result = {"state":"lookup all elb in account" , "data": []}
        for account_i in range(len(self.elb_list)):
            client = self.elb_list[account_i]["client"]
            print(client)
            elb_response = client.describe_load_balancers()['LoadBalancers']
            for i in range (len(elb_response)):
                lbArn = elb_response[i]["LoadBalancerArn"]
                tgState, tgDic = self.get_target_group_state(client,lbArn)

                result["data"].append({
                    "Account" : self.elb_list[account_i]["account_name"],
                    "Name" : elb_response[i]["LoadBalancerName"],
                    "DNS" : elb_response[i]["DNSName"],
                    "TYPE" : elb_response[i]["Type"],
                    "TGState" : tgState,
                    "TGCount": len(tgDic),
                    ## 안보여지는 정보
                    "LoadBalancerArn" : lbArn,
                    "TGDic" : tgDic
                })
        return result

    # target group 상태
    def get_target_group_state(self, client, loadBalancerArn ):
        # port 별로 Target Group이 존재
        # ELB - TG  - target instance
        #           - target instance
        #           -  ...
        #     - TG
        #       ...
        target_groups_dic = {}
        target_groups_state = []

        # 특정 lb에서의 Target Group들
        target_groups = client.describe_target_groups(
            LoadBalancerArn = loadBalancerArn,
        )["TargetGroups"]
        
        # 특정 LB - Target Group들의 각각의 instance 정보
        for target_group in target_groups:
            targetgroupArn = target_group["TargetGroupArn"]
            targetgroupName = target_group["TargetGroupName"]
            targetgroupPort = target_group["Port"]
            target_groups_dic[targetgroupName] = {
                "Arn": targetgroupArn,
                "Port": targetgroupPort,
                "Target_Instance" : []
                }
            
            targets = client.describe_target_health(
                TargetGroupArn = targetgroupArn
            )["TargetHealthDescriptions"]
            target_unhealthy_count = 0
            for target in targets:
                target_state = target["TargetHealth"]["State"]
                if target_state == "unhealthy":
                    target_unhealthy_count += 1
                target_groups_dic[targetgroupName]["Target_Instance"].append({
                    "Id": target["Target"]["Id"],
                    "HealthCheckPort0": target["HealthCheckPort"],
                    "State": target_state
                })
            target_state_color = self.set_state_color(len(targets),target_unhealthy_count)
            target_groups_dic[targetgroupName]["State"] = target_state_color
            target_groups_state.append((target_state_color, targetgroupPort))


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

