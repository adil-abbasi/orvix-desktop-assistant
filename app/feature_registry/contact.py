FEATURE = {
    "name": "contact",
    "keywords": ["contact", "contact form"],
    "dependencies": [],
    "files": {
        "src/pages/Contact.jsx": '''function Contact() {
  return (
    <section className="page">
      <h1>Contact</h1>
      <textarea placeholder="Your message"></textarea>
      <button>Send</button>
    </section>
  );
}

export default Contact;
'''
    }
}