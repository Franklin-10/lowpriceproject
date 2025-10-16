import React from 'react';
import styles from './ProductCard.module.css';

function ProductCard({ product }) {
  return (
    <div className={styles.productCard}>
      <img
        src={product.image_url}
        alt={product.description}
        className={styles.productImage}
      />
      <div className={styles.productDetails}>
        <h3>
          <a href={product.url} target="_blank" rel="noopener noreferrer">
            {product.description}
          </a>
        </h3>
        <p className={styles.priceTag}>R$ {product.price}</p>
        <p className={styles.sellerTag}>{product.seller}</p>
      </div>
    </div>
  );
}

export default ProductCard;
