import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Menu",
  description: "Explore FoodieHub menu including starters, main course, pizza, burgers, desserts and beverages."
};

const menuSections = [
  {
    title: "Starters",
    description: "Perfect bites to begin your meal.",
    items: [
      ["Paneer Tikka", "Grilled cottage cheese with Indian spices.", "₹199", "🥘", "Veg"],
      ["Chicken 65", "Spicy and crispy South Indian chicken starter.", "₹229", "🍗", "Popular"],
      ["Veg Spring Rolls", "Crispy rolls filled with seasoned vegetables.", "₹149", "🥟", "Veg"]
    ]
  },
  {
    title: "Main Course",
    description: "Comforting and filling signature dishes.",
    items: [
      ["Hyderabadi Biryani", "Aromatic rice with chicken and traditional spices.", "₹299", "🍛", "Best Seller"],
      ["Paneer Butter Masala", "Creamy tomato gravy with soft paneer cubes.", "₹239", "🥘", "Veg"],
      ["Veg Fried Rice", "Rice tossed with vegetables and sauces.", "₹189", "🍚", "Veg"]
    ]
  },
  {
    title: "Pizza & Burgers",
    description: "Cheesy favourites for every mood.",
    items: [
      ["Farmhouse Pizza", "Vegetables, cheese and Italian herbs.", "₹249", "🍕", "Veg"],
      ["Chicken Pizza", "Chicken, cheese, onion and capsicum.", "₹299", "🍕", "Popular"],
      ["Classic Burger", "Patty, lettuce, tomato and signature sauce.", "₹179", "🍔", "Classic"]
    ]
  },
  {
    title: "Desserts & Beverages",
    description: "Sweet treats and refreshing drinks.",
    items: [
      ["Chocolate Brownie", "Warm brownie with chocolate sauce.", "₹129", "🍫", "Sweet"],
      ["Gulab Jamun", "Soft milk dumplings in sugar syrup.", "₹99", "🍮", "Indian"],
      ["Fresh Lime Soda", "Refreshing sweet or salted lime soda.", "₹79", "🥤", "Fresh"]
    ]
  }
];

export default function MenuPage() {
  return (
    <>
      <section className="pageHero menuHero">
        <div className="container">
          <span className="sectionLabel">Freshly Prepared</span>
          <h1>Our Menu</h1>
          <p>Simple, tasty and affordable food choices made for every mood.</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <nav className="menuNav" aria-label="Menu categories">
            {menuSections.map((section) => (
              <a key={section.title} href={`#${section.title.toLowerCase().replaceAll(" ", "-").replace("&", "and")}`}>
                {section.title}
              </a>
            ))}
          </nav>

          {menuSections.map((section) => {
            const sectionId = section.title.toLowerCase().replaceAll(" ", "-").replace("&", "and");
            return (
              <div className="menuGroup" id={sectionId} key={section.title}>
                <div className="menuHeading">
                  <div>
                    <h2>{section.title}</h2>
                    <p>{section.description}</p>
                  </div>
                  <span>{section.items.length} items</span>
                </div>
                <div className="menuGrid">
                  {section.items.map(([name, description, price, icon, tag]) => (
                    <article className="menuCard" key={name}>
                      <div className="menuIcon">{icon}</div>
                      <div className="menuCardContent">
                        <span className="menuTag">{tag}</span>
                        <h3>{name}</h3>
                        <p>{description}</p>
                        <div className="cardFooter">
                          <span className="price">{price}</span>
                          <Link className="smallBtn" href="/contact">Order Now</Link>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="ctaSection">
        <div className="container ctaContent">
          <div>
            <span className="sectionLabel lightLabel">Planning a meal?</span>
            <h2>Reserve your table at FoodieHub.</h2>
            <p>Contact us for dine-in reservations, takeaway or delivery enquiries.</p>
          </div>
          <Link className="btn btnLight" href="/contact">Contact Us</Link>
        </div>
      </section>
    </>
  );
}
