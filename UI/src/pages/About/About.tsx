import { REPO_URL } from "./About.config";

const About = () => {
  return (
    <div>
      <h1>About this Todo App</h1>
      <p>This is a todo app written by omeriss.</p>
      <p>
        The source code is available on{" "}
        <a href={REPO_URL} target="_blank">
          GitHub
        </a>
      </p>
      <p>
        To be honest there is not really a point to this page, I thought the
        page won't look good without a nav bar, and then the navbar looked empty
        without any links. So here we are.
      </p>
    </div>
  );
};

export default About;
