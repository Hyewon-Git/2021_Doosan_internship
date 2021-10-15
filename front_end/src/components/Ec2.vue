<template>
  <div id="ec2_dashboard">
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
            <a> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; </a>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </div>
        </v-card-title>

        <v-data-table
          style="width: 120%"
          :headers="headers"
          :items="contents"
          :search="search"
          
        >
        </v-data-table>
    </v-container>
    </v-sheet>
  </div>
</template>

<script>
    import axios from 'axios';
    
    export default {
        name: 'Elb',
        data: () => ({
            search: '',
            headers: [
                { text: 'Account', value: 'Account' },
                { text: 'Name', value: 'Name' },
                { text: 'DNS', value: 'DNS' },
                { text: 'TYPE', value: 'TYPE' }
            ],
            contents: []
            }),
        created() {
            axios.get('http://localhost:5000')
                .then(res => {
                    console.log(res)

                    const data = res.data
                    this.contents = data["data"]
                })
                .catch(error => console.log(error))
        }
    }
</script>