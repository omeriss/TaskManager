import TaskCard from "../../components/Task/Task";
import styles from "./HomePage.module.css";
import { useQuery } from "@tanstack/react-query";
import routes from "../../api/api";
import { Spin, Input, Select, DatePicker, Button } from "antd";
import { TaskStatus, type Task } from "../../interfaces/Task";
import { useMemo, useState } from "react";
import type { TaskFilters } from "../../interfaces/TaskFilters";
import dayjs from "dayjs";

const { RangePicker } = DatePicker;

type SortField = "status" | "created_at" | "due_date";

const HomePage = () => {
  const [filters, setFilters] = useState<TaskFilters>({});
  const [sortField, setSortField] = useState<SortField>("created_at");

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["tasks", filters],
    queryFn: async () => {
      const res = await routes.getAllTasks(filters);

      return res.data;
    },
  });

  const tasks = useMemo(() => {
    const tasks: Task[] = data ? [...data] : [];

    return tasks.sort((a, b) => {
      if (sortField === "status") {
        return a.status === TaskStatus.PENDING ? -1 : 1;
      }

      if (sortField === "created_at") {
        return (
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        );
      }

      if (sortField === "due_date") {
        const aDate = a.due_date
          ? new Date(a.due_date).getTime()
          : Number.MAX_SAFE_INTEGER;
        const bDate = b.due_date
          ? new Date(b.due_date).getTime()
          : Number.MAX_SAFE_INTEGER;
        return aDate - bDate;
      }

      return 0;
    });
  }, [data, sortField]);

  if (isError)
    return <div className={styles.noneContainer}>Error: {error?.message}</div>;

  return (
    <div className={styles.tasksContainer}>
      <div className={styles.filters}>
        <div>
          <Input
            placeholder="Search by title"
            onChange={(value) =>
              setFilters((prev) => ({
                ...prev,
                title_contains: value.target.value ?? undefined,
              }))
            }
            value={filters.title_contains}
          />

          <Select
            placeholder="Filter by status"
            allowClear
            onChange={(value) =>
              setFilters((prev) => ({ ...prev, status: value }))
            }
            value={filters.status}
          >
            <Select.Option value={TaskStatus.PENDING}>Pending</Select.Option>
            <Select.Option value={TaskStatus.COMPLETED}>
              Completed
            </Select.Option>
          </Select>

          <RangePicker
            onChange={(dates) => {
              if (dates) {
                setFilters((prev) => ({
                  ...prev,
                  from_date: dates[0]?.toISOString(),
                  to_date: dates[1]?.toISOString(),
                }));
              } else {
                setFilters((prev) => ({
                  ...prev,
                  from_date: undefined,
                  to_date: undefined,
                }));
              }
            }}
            value={
              filters.from_date && filters.to_date
                ? [dayjs(filters.from_date), dayjs(filters.to_date)]
                : undefined
            }
            placeholder={["Created From", "Created To"]}
          />

          <Select
            placeholder="Sort by"
            value={sortField}
            onChange={(value) => setSortField(value as SortField)}
          >
            <Select.Option value="status">Status</Select.Option>
            <Select.Option value="created_at">Created Date</Select.Option>
            <Select.Option value="due_date">Due Date</Select.Option>
          </Select>
          <Button type="primary" href="/api/tasks/summary">
            Download Summary
          </Button>
        </div>
      </div>

      {isLoading && (
        <div className={styles.noneContainer}>
          <Spin tip="Loading tasks…" />
        </div>
      )}

      {tasks.length === 0 ? (
        !isLoading && <div className={styles.noneContainer}>No tasks yet</div>
      ) : (
        <div className={styles.grid}>
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  );
};

export default HomePage;
