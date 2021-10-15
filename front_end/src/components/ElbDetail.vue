<template>
  <div id="elb_detail_dashboard">
    <v-sheet
      id="scrolling-techniques-3"
      class="overflow-y-auto"
      max-height="700"
    >
      <v-container >
        <v-card
          class="mx-auto"
          max-width="1900px">
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-subtitle>ELB detail page</v-list-item-subtitle>
              <v-list-item-title class="text-h5">
                <b>{{ elbDetail.Name }}</b>
              </v-list-item-title>
              
              <v-divider></v-divider>
              <ul class="text-body-2">
                <li><b>Account</b> : {{ elbDetail.Account }}</li>
                <li><b>DNS</b>&emsp;&emsp; : {{ elbDetail.DNS }}</li>
                <li><b>ARN</b>&emsp;&emsp; : {{ elbDetail.LoadBalancerArn }}</li>
                <li><b>TYPE</b>&emsp;&nbsp;&nbsp; : {{ elbDetail.TYPE }}</li>
                <li><b>Target Groups</b></li>
              </ul>
            </v-list-item-content>
          </v-list-item>


          <v-data-table
            :headers="headers"
            :items="contents"
            :hide-default-footer=true
            class="elbDetail"
            
          >
            <template v-slot:item.Port="{ item }">
              <v-chip
                :color="item.State"
                text-color="white"
                small
                style="padding : 0 5px; margin: 0.5px 0.5px 0.5px "
              >
                {{ item.Port }}
              </v-chip>
            </template>
            <template v-slot:item.Target_Instance="{ item }">
              <a
                v-for="instance in item.Target_Instance"
                :key="instance"
              >
                <v-chip
                  :color="instance.State"
                  text-color="white"
                  small
                  style="padding : 0 5px; margin: 0.5px 0.5px 0.5px"
                  >
                  {{ instance.HealthCheckPort0 }}
                </v-chip>
                {{ instance.Name }}
              </a>
              <!-- <v-data-iterato
                :items="item.Target_Instance">
                <v-row>
                  <v-col
                    v-for="i in item.Target_Instance "
                    :key="i"
                  >
                    <v-card>
                      <v-list>
                        <p><b>ID</b>{{ i.Id }}</p>
                      </v-list>
                    </v-card>
                  </v-col>
                </v-row>
              </v-data-iterato> -->
            </template>
          </v-data-table>
        </v-card>
        
      </v-container>
    </v-sheet>
  </div>
</template>

<script>
  export default {
    name: 'ElbDetail',
    data: () => ({
      elbDetail: {},
      headers: [
          { text: 'Port', value: 'Port' ,width: '100px'},
          { text: 'Name', value: 'Name' , widht: '150px' },
          { text: 'Protocol', value: 'Protocol', width: "80" },
          
          { text: 'Target Instance  ( HealthCheckPort / Name )', value: 'Target_Instance',width: '700px' },
      ],
      contents: []
      
    }),
    created() {
      const data = this.$route.params.data
      this.elbDetail = data
      this.contents = data.TGDic

    }
  }
</script>