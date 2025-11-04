import axios from "axios";
import { APP_API_URL } from "./api.config";
import type { TaskCreate } from "../interfaces/TaskCreate";
import type { Task } from "../interfaces/Task";
import type { TaskFilters } from "../interfaces/TaskFilters";

const api = axios.create({
  baseURL: APP_API_URL,
});

const routes = {
  getAllTasks: (filters?: TaskFilters) =>
    api.get<Task[]>("/api/tasks", { params: filters }),
  createTask: (taskData: TaskCreate) => api.post("/api/tasks", taskData),
  setCompleted: (taskId: number) => api.patch(`/api/tasks/${taskId}/complete`),
  deleteTask: (taskId: number) => api.delete(`/api/tasks/${taskId}`),
};

export default routes;
