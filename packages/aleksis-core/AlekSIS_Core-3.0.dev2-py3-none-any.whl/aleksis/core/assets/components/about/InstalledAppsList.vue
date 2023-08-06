<template>
  <ApolloQuery :query="require('./installedApps.graphql')">
    <template #default="{ result: { error, data }, isLoading }">
      <v-row v-if="isLoading">
        <v-col
          v-for="idx in 3"
          :key="idx"
          cols="12"
          md="6"
          lg="6"
          xl="4"
          class="d-flex align-stretch"
        >
          <v-card class="d-flex flex-column flex-grow-1 pa-4">
            <v-skeleton-loader
              type="heading, actions, text@5"
            ></v-skeleton-loader>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-if="data.installedApps">
        <installed-app-card
          v-for="app in data.installedApps"
          :key="app.name"
          :app="app"
        />
      </v-row>
    </template>
  </ApolloQuery>
</template>

<script>
import InstalledAppCard from "./InstalledAppCard.vue";

export default {
  name: "InstalledAppsList",
  components: { InstalledAppCard },
};
</script>
