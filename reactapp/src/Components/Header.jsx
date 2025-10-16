import styles from "./Header.module.css"

const Header = () => {
  return (
    <header>
      <nav>
        <h1 className={styles.logo}>LOWPRICEPROJECT</h1>
      </nav>
    </header>
  );
};

export default Header;
