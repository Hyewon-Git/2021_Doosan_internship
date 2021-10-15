<template>
  <div id="elb_dashboard">
    <v-sheet
      id="scrolling-techniques-3"
      class="overflow-y-auto"
      max-height="700"
    >
    <v-container>
        <v-card-title>
          <div style="display: flex; width: 100%">
            
            <v-select
              v-model="search"
              :items="['di-prd', 'div-prd']"
              label="Account"
              stye="width: 3px"
            ></v-select>
            <a> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</a>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <a> &emsp;</a>
            <v-btn
              class="btn" 
              @click="refresh"
              color="#cce7f5"
              elevation="4"
            >Refresh</v-btn>
          </div>
        </v-card-title>
        
        <v-data-table
          style="width: 120%"
          :headers="headers"
          :items="contents"
          :search="search"
          @click:row="detailElb"
          class="elb"
          :loading="loading"
        >
          <template v-slot:item.TGState="{ item }">
            <v-chip
              v-for="port in item.TGState"
              :key="port"
              :color="port[0]"
              text-color="white"
              small
              style="padding : 0 5px; margin: 1px 2px 1px"
            >
              {{ port[1] }}
            </v-chip>

          </template>
          
        </v-data-table>
    </v-container>
    </v-sheet>

  </div>
</template>

<script>
    import axios from 'axios';
    import router from '../router/index'
    
    export default {
        props: ["name"],
        name: 'Elb',
        data: () => ({
            search: '',
            headers: [
                { text: 'Account', value: 'Account',width: '100px'},
                { text: 'Name', value: 'Name' },
                { text: 'DNS', value: 'DNS' },
                { text: 'TYPE', value: 'TYPE', width: '80px' },
                { text: 'Target Group State', value: 'TGState',width: '280px' },
                
            ],
            contents: [],
            is_show: false,
            loading: true,
            }),
        created() {
            axios.get('http://localhost:5000/elb')
                .then(res => {
                    console.log(res)

                    const data = res.data
                    this.contents = data["data"]
                })
                .catch(error => console.log(error))
                .finally(() => {
                  this.loading = false;
                })
        },
        methods : {
          detailElb: function (row) {
            const elbname = row.Name
            console.log("hello.", elbname)
            console.log("row", row)
            this.is_show = !this.is_show;
            router.push({
              name: "ElbDetail",
              params: { name: elbname, data: row , a:row["Name"]}
            })
          },
          refresh: function(){
            console.log("Refresh")
            this.loading= true;
            axios.post('http://localhost:5000/elb', {body:{refresh: "true"}})
              .then(res =>{
                console.log(res.data)
              })
              .catch(error => console.log(error))
              .finally(() => {
                this.loading = false;
              })
          }
        }
    }
</script>

<style>
.v-data-table-header{
  background-color: #cce7f5;
}

</style>