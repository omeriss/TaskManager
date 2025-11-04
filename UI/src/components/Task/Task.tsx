import { TaskStatus, type Task } from "../../interfaces/Task";
import styles from "./Task.module.css";
import { Button, Popconfirm, Card, Tag, Descriptions } from "antd";
import {
  CheckOutlined,
  DeleteOutlined,
  ClockCircleOutlined,
  CalendarOutlined,
} from "@ant-design/icons";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import routes from "../../api/api";
import { toast } from "react-toastify";

interface TaskProps {
  task: Task;
}

const TaskCard = ({ task }: TaskProps) => {
  const queryClient = useQueryClient();

  const completeMutation = useMutation({
    mutationFn: () => routes.setCompleted(task.id),
    onSuccess: () => {
      toast.success("Task completed successfully");
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
    onError: () => {
      toast.error("Failed to complete task");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => routes.deleteTask(task.id),
    onSuccess: () => {
      toast.success("Task deleted successfully");
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
    onError: () => {
      toast.error("Failed to delete task");
    },
  });

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "—";

    try {
      const d = new Date(dateString);
      return d.toLocaleString();
    } catch {
      return dateString;
    }
  };

  return (
    <Card
      title={
        <div className={styles.header}>
          <h4>{task.title}</h4>
          <Tag
            color={task.status === TaskStatus.COMPLETED ? "success" : "warning"}
          >
            {task.status}
          </Tag>
        </div>
      }
      className={styles.card}
    >
      <p className={styles.description}>
        {task.description ?? "No description"}
      </p>

      <Descriptions size="small" column={2}>
        <Descriptions.Item
          label={
            <div>
              <ClockCircleOutlined /> Due
            </div>
          }
        >
          {formatDate(task.due_date)}
        </Descriptions.Item>
        <Descriptions.Item
          label={
            <div>
              <CalendarOutlined /> Created
            </div>
          }
        >
          {formatDate(task.created_at)}
        </Descriptions.Item>
      </Descriptions>

      <div className={styles.actions}>
        {task.status !== TaskStatus.COMPLETED && (
          <Button
            type="primary"
            icon={<CheckOutlined />}
            onClick={() => completeMutation.mutate()}
            loading={completeMutation.isPending}
          >
            Complete
          </Button>
        )}
        <Popconfirm
          title="Delete task"
          description="Are you sure you want to delete this task?"
          onConfirm={() => deleteMutation.mutate()}
          okText="Yes"
          cancelText="No"
        >
          <Button
            danger
            icon={<DeleteOutlined />}
            loading={deleteMutation.isPending}
          >
            Delete
          </Button>
        </Popconfirm>
      </div>
    </Card>
  );
};

export default TaskCard;
