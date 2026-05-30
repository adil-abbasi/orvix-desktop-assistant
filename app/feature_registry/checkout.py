FEATURE = {
    "name": "checkout",
    "keywords": ["checkout", "payment"],
    "dependencies": [],
    "files": {
        "src/pages/Checkout.jsx": '''function Checkout() {
  return (
    <section className="page">
      <h1>Checkout</h1>
      <p>Payment and order confirmation will be handled here.</p>
    </section>
  );
}

export default Checkout;
'''
    }
}