import "@mdi/font/css/materialdesignicons.css";

import "./util";
import "./app";

import CeleryProgress from "./components/celery_progress/CeleryProgress.vue";
import About from "./components/about/About.vue";

window.router.addRoute({
  path: "/celery_progress/:taskId",
  component: CeleryProgress,
  props: true,
  name: "core.celery_progress",
});
window.router.addRoute({
  path: "/about",
  component: About,
  name: "core.about",
});
