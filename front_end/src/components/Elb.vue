<template>
  <div id="elb_dashboard">
    <p>AWS Elastic LoadBalancers: {{ elbList }}</p>
    <v-container>
    <v-data-table
            style="width: 50%"
            :headers="headers"
            :items="contents"
    ></v-data-table>
  </v-container>
  </div>
</template>

<script>
    import axios from 'axios';
    
    export default {
        name: 'Elb',
        data: () => ({
            headers: [
                { text: 'ID', value: 'id' },
                { text: 'Name', value: 'name' },
                { text: 'Food', value: 'food' },
            ],
            contents: [
                { id: 1, name: 'ABC', food: 'pizza' },
                { id: 2, name: 'DEF', food: 'chicken' },
                { id: 3, name: 'GHI', food: 'hamburger' },
            ]
            }),
        created() {
            axios.get('http://localhost:5000/elb')
                .then(res => {
                    console.log(res)

                    const data = res.data
                    this.contents = data["data"]
                    
                    const datas = []
                    // 오브젝트를 순회하여 key값을 얻어내고
                    // 원하는 데이터만 배열에 다시 밀어넣는다
                    // 이 과정에서 key값은 id 프로퍼티에 추가함!
                    for(let key in data) {
                        const elb = data[key]
                        elb.name = key
                        datas.push(elb)
                    }
                    console.log(datas)
                  // 이메일 값만 추출하여 데이터를 업데이트
                    this.email = datas[0].LoadBalancers
                })
                .catch(error => console.log(error))
        }
    }
</script>