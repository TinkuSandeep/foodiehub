import Link from "next/link";

const dishes = [
  {
    name: "Hyderabadi Biryani",
    description: "Aromatic basmati rice cooked with spices and tender chicken.",
    price: "₹299",
    image: "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?auto=format&fit=crop&w=900&q=80"
  },
  {
    name: "Farmhouse Pizza",
    description: "Loaded with fresh vegetables, cheese and Italian herbs.",
    price: "₹249",
    image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=80"
  },
  {
    name: "Classic Burger",
    description: "Juicy patty, fresh lettuce, tomato and signature sauce.",
    price: "₹179",
    image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80"
  }
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="container heroContent">
          <span className="eyebrow">Fresh • Tasty • Affordable</span>
          <h1>Delicious food for every mood.</h1>
          <p>Enjoy freshly prepared dishes made with quality ingredients and served with care.</p>
          <Link className="btn" href="/menu">Explore Our Menu</Link>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="sectionTitle">
            <h2>Featured Dishes</h2>
            <p>Our customer favourites, prepared fresh every day.</p>
          </div>
          <div className="grid">
            {dishes.map((dish) => (
              <article className="card" key={dish.name}>
                <img src={dish.image} alt={dish.name} />
                <div className="cardBody">
                  <h3>{dish.name}</h3>
                  <p>{dish.description}</p>
                  <span className="price">{dish.price}</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section sectionAlt">
        <div className="container">
          <div className="sectionTitle">
            <h2>Why Choose Us?</h2>
            <p>Simple reasons why our customers enjoy FoodieHub.</p>
          </div>
          <div className="featureGrid">
            <div className="feature"><span>🥗</span><h3>Fresh Ingredients</h3><p>We use fresh and quality ingredients.</p></div>
            <div className="feature"><span>👨‍🍳</span><h3>Expert Chefs</h3><p>Every dish is prepared with care.</p></div>
            <div className="feature"><span>🚚</span><h3>Fast Service</h3><p>Quick dine-in, takeaway and delivery.</p></div>
          </div>
        </div>
      </section>
    </>
  );
}
