import axios from "axios";
import { APP_API_URL } from "./api.config";

const api = axios.create({
  baseURL: APP_API_URL,
});

const routes = {
  getAllTasks: () => api.get("/api/tasks"),
};

export default routes;
