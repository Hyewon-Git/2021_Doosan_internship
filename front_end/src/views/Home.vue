<template>
  <v-card class="overflow-hidden">
    <v-app-bar
      color="#0088CE"
      dark
      shrink-on-scroll
      scroll-target="#scrolling-techniques-3"
    >
      <router-link to="/">
        <v-app-bar-title width="300px" style="margin:130px 0px;" > Doosan AWS </v-app-bar-title>
      </router-link>

      <v-spacer></v-spacer>

      <template v-slot:extension>
        <v-tabs
          align-with-title
          class="ml-n9"
          color="white"
        >
          <v-tab
            v-for="tab in tabs"
            :key="tab"
            :to="tab.route"
          >
            {{ tab.name }}
          </v-tab>

          <v-tab-item 
            v-for="tab of tabs"
            :key="tab"
            :value="tab.route"
          >
            <router-view></router-view>
          </v-tab-item>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-sheet
      id="scrolling-techniques-3"
      class="overflow-y-auto"
      max-height="675"
    >
      <v-container style="height: 1000px;"></v-container>
    </v-sheet>
  </v-card>
</template>

<script>

export default {
  name: 'Home',
  data: () => ({
      activeTab: '/',
      tabs: [
        { id: 1, name: 'EC2', route: '/ec2' },
        { id: 2, name: 'ELB', route: '/elb' }
      ],
    }),
}
</script>

<style>
.v-app-bar-title__content{width: 300px;color:white;font-weight:bold;}
</style>