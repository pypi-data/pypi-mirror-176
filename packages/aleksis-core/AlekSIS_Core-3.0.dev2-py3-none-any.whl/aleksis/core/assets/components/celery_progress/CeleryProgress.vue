<template>
  <v-row>
    <v-col sm="0" md="1" lg="2" xl="3" />
    <v-col sm="12" md="10" lg="8" xl="6">
      <v-card :loading="$apollo.loading">
        <v-card-title v-if="progress">
          {{ progress.meta.title }}
        </v-card-title>
        <v-card-text v-if="progress">
          <v-progress-linear
            :value="progress.progress.percent"
            buffer-value="0"
            color="primary"
            class="mb-2"
            stream
          />
          <div class="text-center mb-4">
            {{
              progress.meta.progressTitle
                ? progress.meta.progressTitle
                : $t("celery_progress.progress_title")
            }}
          </div>
          <div v-if="progress">
            <message-box
              v-for="(message, idx) in progress.messages"
              dense
              :type="message.tag"
              transition="slide-x-transition"
              :key="idx"
            >
              {{ message.message }}
            </message-box>
          </div>
          <message-box
            v-if="progress.state === 'ERROR'"
            dense
            type="error"
            transition="slide-x-transition"
          >
            {{
              progress.meta.errorMessage
                ? progress.meta.errorMessage
                : $t("celery_progress.error_message")
            }}
          </message-box>
          <message-box
            v-if="progress.state === 'SUCCESS'"
            dense
            type="success"
            transition="slide-x-transition"
          >
            {{
              progress.meta.successMessage
                ? progress.meta.successMessage
                : $t("celery_progress.success_message")
            }}
          </message-box>
        </v-card-text>
        <v-card-actions
          v-if="
            progress &&
            (progress.state === 'ERROR' || progress.state === 'SUCCESS')
          "
        >
          <back-button :href="progress.meta.backUrl" text />
          <v-spacer />
          <v-btn
            v-if="progress.meta.additionalButton"
            :href="progress.meta.additionalButton.url"
            text
            color="primary"
          >
            <v-icon v-if="progress.meta.additionalButton.icon" left>
              {{ progress.meta.additionalButton.icon }}
            </v-icon>
            {{ progress.meta.additionalButton.title }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col sm="0" md="1" lg="2" xl="3" />
  </v-row>
</template>

<script>
import BackButton from "../BackButton.vue";
import MessageBox from "../MessageBox.vue";

export default {
  name: "CeleryProgress",
  components: { BackButton, MessageBox },
  apollo: {
    celeryProgressByTaskId: {
      query: require("./celeryProgress.graphql"),
      variables() {
        return {
          taskId: this.$route.params.taskId,
        };
      },
      pollInterval: 1000,
    },
  },
  computed: {
    progress() {
      return this.celeryProgressByTaskId;
    },
    state() {
      return this.progress ? this.progress.state : null;
    },
  },
  watch: {
    state(newState) {
      if (newState === "SUCCESS" || newState === "ERROR") {
        this.$apollo.queries.celeryProgressByTaskId.stopPolling();
        this.$apollo.mutate({
          mutation: require("./celeryProgressFetched.graphql"),
          variables: {
            taskId: this.$route.params.taskId,
          },
        });
      }
      if (newState === "SUCCESS" && this.progress.meta.redirectOnSuccessUrl) {
        window.location.replace(this.progress.meta.redirectOnSuccessUrl);
        // FIXME this.$router.push(this.progress.meta.redirectOnSuccessUrl);
      }
    },
  },
};
</script>
