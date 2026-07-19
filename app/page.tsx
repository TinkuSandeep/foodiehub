import Link from "next/link";

const categories = [
  { name: "Starters", icon: "🥟", text: "Crispy and flavourful bites" },
  { name: "Main Course", icon: "🍛", text: "Wholesome Indian favourites" },
  { name: "Pizza & Burgers", icon: "🍕", text: "Cheesy comfort food" },
  { name: "Desserts", icon: "🍰", text: "A sweet finish to every meal" }
];

const dishes = [
  {
    name: "Hyderabadi Biryani",
    category: "Main Course",
    description: "Aromatic basmati rice cooked with spices and tender chicken.",
    price: "₹299",
    image: "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?auto=format&fit=crop&w=900&q=80"
  },
  {
    name: "Farmhouse Pizza",
    category: "Pizza",
    description: "Loaded with fresh vegetables, cheese and Italian herbs.",
    price: "₹249",
    image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=80"
  },
  {
    name: "Classic Burger",
    category: "Burger",
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
          <p>
            Enjoy freshly prepared dishes made with quality ingredients,
            authentic flavours and warm hospitality.
          </p>
          <div className="heroActions">
            <Link className="btn" href="/menu">Explore Our Menu</Link>
            <Link className="btn btnSecondary" href="/contact">Book a Table</Link>
          </div>
          <div className="heroStats">
            <span><strong>20+</strong> Dishes</span>
            <span><strong>4.8/5</strong> Customer Rating</span>
            <span><strong>30 min</strong> Quick Service</span>
          </div>
        </div>
      </section>

      <section className="section sectionAlt">
        <div className="container">
          <div className="sectionTitle">
            <span className="sectionLabel">Browse Categories</span>
            <h2>Something tasty for everyone</h2>
            <p>Choose from our popular food categories and discover your next favourite dish.</p>
          </div>
          <div className="categoryGrid">
            {categories.map((category) => (
              <Link className="categoryCard" href="/menu" key={category.name}>
                <span>{category.icon}</span>
                <h3>{category.name}</h3>
                <p>{category.text}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="sectionTitle">
            <span className="sectionLabel">Customer Favourites</span>
            <h2>Featured Dishes</h2>
            <p>Popular dishes prepared fresh every day using quality ingredients.</p>
          </div>
          <div className="grid">
            {dishes.map((dish) => (
              <article className="card dishCard" key={dish.name}>
                <div className="imageWrap">
                  <img src={dish.image} alt={dish.name} />
                  <span className="dishBadge">{dish.category}</span>
                </div>
                <div className="cardBody">
                  <h3>{dish.name}</h3>
                  <p>{dish.description}</p>
                  <div className="cardFooter">
                    <span className="price">{dish.price}</span>
                    <Link className="smallBtn" href="/menu">View Menu</Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
          <div className="centerAction">
            <Link className="btn" href="/menu">View Full Menu</Link>
          </div>
        </div>
      </section>

      <section className="section sectionAlt">
        <div className="container">
          <div className="sectionTitle">
            <span className="sectionLabel">Why FoodieHub</span>
            <h2>Good food, made simple</h2>
            <p>Simple reasons why our customers enjoy dining with FoodieHub.</p>
          </div>
          <div className="featureGrid">
            <div className="feature"><span>🥗</span><h3>Fresh Ingredients</h3><p>We use fresh, carefully selected ingredients in every dish.</p></div>
            <div className="feature"><span>👨‍🍳</span><h3>Expert Chefs</h3><p>Every meal is prepared with care, consistency and flavour.</p></div>
            <div className="feature"><span>🚚</span><h3>Fast Service</h3><p>Quick dine-in, takeaway and delivery without compromising quality.</p></div>
          </div>
        </div>
      </section>

      <section className="ctaSection">
        <div className="container ctaContent">
          <div>
            <span className="sectionLabel lightLabel">Hungry already?</span>
            <h2>Discover your next favourite meal.</h2>
            <p>Explore our complete menu and enjoy fresh food made for every mood.</p>
          </div>
          <Link className="btn btnLight" href="/menu">Explore Menu</Link>
        </div>
      </section>
    </>
  );
}
