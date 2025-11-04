import { Modal, Form, Input, DatePicker, Button } from "antd";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { TaskCreate } from "../../interfaces/TaskCreate";
import api from "../../api/api";
import styles from "./NewTaskModal.module.css";
import { toast } from "react-toastify";
import { useState } from "react";

interface NewTaskModalProps {
  children?: React.ReactNode;
}

const NewTaskModal = ({ children }: NewTaskModalProps) => {
  const [form] = Form.useForm();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);

  const createTaskMutation = useMutation({
    mutationFn: (taskData: TaskCreate) => api.createTask(taskData),
    onSuccess: () => {
      toast.success("Task created successfully");
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      form.resetFields();
      setOpen(false);
    },
    onError: () => {
      toast.error("Failed to create task");
    },
  });

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();

      const taskData: TaskCreate = {
        title: values.title,
        description: values.description,
        due_date: values.due_date?.toISOString() ?? null,
      };

      createTaskMutation.mutate(taskData);
    } catch {
      toast.error("Please correct the errors in the form");
    }
  };

  return (
    <>
      <Modal
        title="Create New Task"
        open={open}
        onCancel={() => setOpen(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          className={styles.modalForm}
          preserve={false}
        >
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true, message: "Please enter the task title" }]}
            className={styles.formItem}
          >
            <Input placeholder="Enter task title" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[
              { required: true, message: "Please enter the task description" },
            ]}
            className={styles.formItem}
          >
            <Input.TextArea placeholder="Enter task description" />
          </Form.Item>

          <Form.Item
            name="due_date"
            label="Due Date"
            className={styles.formItem}
          >
            <DatePicker
              showTime
              className={styles.datePicker}
              placeholder="Select due date and time"
            />
          </Form.Item>

          <div className={styles.actions}>
            <Button onClick={() => setOpen(false)}>Cancel</Button>
            <Button
              type="primary"
              onClick={handleSubmit}
              loading={createTaskMutation.isPending}
            >
              Create Task
            </Button>
          </div>
        </Form>
      </Modal>
      <div onClick={() => setOpen(true)}>{children}</div>
    </>
  );
};

export default NewTaskModal;
