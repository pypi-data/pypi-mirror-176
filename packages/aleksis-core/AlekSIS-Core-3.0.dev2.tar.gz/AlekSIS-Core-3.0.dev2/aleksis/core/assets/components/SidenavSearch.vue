<script>
export default {
  methods: {
    submit: function () {
      this.$refs.form.submit();
    },
  },
  props: {
    action: {
      type: String,
      required: true,
    },
  },
  name: "SidenavSearch",
  data() {
    return {
      q: "",
    };
  },
};
</script>

<template>
  <ApolloQuery
    :query="require('./searchSnippets.graphql')"
    :variables="{
      q,
    }"
    :skip="!q"
  >
    <template #default="{ result: { error, data }, isLoading, query }">
      <form method="get" ref="form" :action="action" id="search-form">
        <input type="hidden" name="q" :value="q" />
        <v-autocomplete
          :prepend-icon="'mdi-magnify'"
          append-icon=""
          @click:prepend="submit"
          single-line
          clearable
          :loading="!!isLoading"
          id="search"
          type="search"
          enterkeyhint="search"
          :label="$t('actions.search')"
          :search-input.sync="q"
          flat
          solo
          cache-items
          hide-no-data
          hide-details
          :items="data ? data.searchSnippets : undefined"
        >
          <template #item="{ item }">
            <v-list-item :href="item.obj.absoluteUrl">
              <v-list-item-icon v-if="item.obj.icon">
                <v-icon>{{ "mdi-" + item.obj.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title> {{ item.obj.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.text }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-autocomplete>
      </form>
    </template>
  </ApolloQuery>
</template>
