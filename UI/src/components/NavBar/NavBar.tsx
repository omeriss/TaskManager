import { Link } from "react-router-dom";
import { Layout, Menu, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import styles from "./NavBar.module.css";
import { NAVBAR_ITEMS } from "./NavBar.config";
import NewTaskModal from "../NewTaskModal/NewTaskModal";

const { Header } = Layout;

const NavBar = () => {
  return (
    <Header className={styles.nav}>
      <div>
        <div className={styles.logoContainer}>
          <img src="/logo-imgonly.png" className={styles.logo} />
          <Link to="/" className={styles.title}>
            Task Manager
          </Link>
        </div>

        <Menu
          theme="dark"
          mode="horizontal"
          selectable={false}
          items={NAVBAR_ITEMS.map((item) => ({
            key: item.key,
            label: <Link to={item.link}>{item.label}</Link>,
          }))}
          className={styles.links}
        />

        <div className={styles.actions}>
          <NewTaskModal>
            <Button type="primary" icon={<PlusOutlined />}>
              New Task
            </Button>
          </NewTaskModal>
        </div>
      </div>
    </Header>
  );
};

export default NavBar;
