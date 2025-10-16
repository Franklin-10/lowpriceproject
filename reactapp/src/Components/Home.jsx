import { useMemo, useState } from 'react';
import ProductCard from './Produto/ProductCard'
import useFetch from './Hooks/useFetch';
import Error from './Helper/Error';
import styles from './Home.module.css';
import Loading from './Helper/Loading';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [products, setProducts] = useState([]);
  const [status, setStatus] = useState('idle');

  const { request, loading, error } = useFetch();

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!searchTerm) return;
    setStatus('searching');
    setProducts([]);

    const { json: startData } = await request(
      `/search/?search=${encodeURIComponent(searchTerm)}`,
    );

    if (startData && startData.status === 'ok') {
      pollForResults(startData.search_id);
    } else {
      setStatus('error');
    }
    console.log('Busca iniciada com sucesso:', searchTerm);
  };

  const pollForResults = (search_id) => {
    const pollingInterval = setInterval(async () => {
      const { json: resultsData } = await request(`/api/results/${search_id}/`);

      if (resultsData) {
        if (resultsData.status === 'done') {
          clearInterval(pollingInterval);
          const allProducts = Object.values(
            resultsData.products_by_seller,
          ).flat();
          setProducts(allProducts);
          setStatus('done');
          console.log(resultsData);
          console.log(allProducts);
          console.log(Object.keys(resultsData.products_by_seller));
        } else if (resultsData.status === 'error') {
          clearInterval(pollingInterval);
          setStatus('error');
        }
      }
    }, 3000);
  };

  const cheapestProduct = useMemo(() => {
    if (products.length === 0) return null;

    const minPrice = Math.min(...products.map((p) => Number(p.price)));

    return products.find((p) => Number(p.price) === minPrice);
  }, [products]);

  return (
    <>
      <main className={styles.mainContainer}>
        <h1>DIGITE SEU PRODUTO</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ex: Placa de Video RTX 4070"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            disabled={status === 'searching'}
          />
          <button type="submit" disabled={status === 'searching'}>
            {status === 'searching' ? 'Buscando...' : 'PESQUISAR'}
          </button>
        </form>
        {status === 'error' && <Error error={error} />}
        {status === 'searching' && <Loading />}
        {status === 'done' && cheapestProduct && (
        <div id="results-container">
            <div className={styles.minPrice}>
              <p className={styles.title}>MAIS BARATO</p>
              <ProductCard product={cheapestProduct} />
            </div>
          
          <h1 className={styles.title}> CONFIRA OUTRAS OFERTAS</h1>
          <div className={`${styles.productsList} ${styles.productsListEcommerceB}` }>
            {products.length > 0 ? (
              products
                .filter((product) => product.seller === 'ecommerceB')
                .map((product) => (
                  <ProductCard key={product.url} product={product} />
                ))
            ) : (
              <p>Erro ao buscar produtos do EcommerceB</p>
            )}
          </div>
          <div className={`${styles.productsList} ${styles.productsListEcommerceA}` }>
            {products.length > 0 ? (
              products
                .filter((product) => product.seller === 'ecommerceA')
                .map((product) => (
                  <ProductCard key={product.url} product={product} />
                ))
            ) : (
              <p>Erro ao buscar produtos do EcommerceA</p>
            )}
          </div>
        </div>
        )}
      </main>
    </>
  );
}

export default App;
