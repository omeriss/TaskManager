import type { TaskStatus } from "./Task";

interface TaskFilters {
  status?: TaskStatus;
  from_date?: string;
  to_date?: string;
  title_contains?: string;
}

export type { TaskFilters };
