import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Menu",
  description: "Explore FoodieHub menu including starters, main course, biryani, pizza, desserts and beverages."
};

const menuSections = [
  {
    title: "Starters",
    items: [
      ["Paneer Tikka", "Grilled cottage cheese with Indian spices.", "₹199"],
      ["Chicken 65", "Spicy and crispy South Indian chicken starter.", "₹229"],
      ["Veg Spring Rolls", "Crispy rolls filled with seasoned vegetables.", "₹149"]
    ]
  },
  {
    title: "Main Course",
    items: [
      ["Hyderabadi Biryani", "Aromatic rice with chicken and traditional spices.", "₹299"],
      ["Paneer Butter Masala", "Creamy tomato gravy with soft paneer cubes.", "₹239"],
      ["Veg Fried Rice", "Rice tossed with vegetables and sauces.", "₹189"]
    ]
  },
  {
    title: "Pizza & Burgers",
    items: [
      ["Farmhouse Pizza", "Vegetables, cheese and Italian herbs.", "₹249"],
      ["Chicken Pizza", "Chicken, cheese, onion and capsicum.", "₹299"],
      ["Classic Burger", "Patty, lettuce, tomato and signature sauce.", "₹179"]
    ]
  },
  {
    title: "Desserts & Beverages",
    items: [
      ["Chocolate Brownie", "Warm brownie with chocolate sauce.", "₹129"],
      ["Gulab Jamun", "Soft milk dumplings in sugar syrup.", "₹99"],
      ["Fresh Lime Soda", "Refreshing sweet or salted lime soda.", "₹79"]
    ]
  }
];

export default function MenuPage() {
  return (
    <>
      <section className="pageHero">
        <div className="container">
          <h1>Our Menu</h1>
          <p>Simple, tasty and affordable food choices.</p>
        </div>
      </section>
      <section className="section">
        <div className="container">
          {menuSections.map((section) => (
            <div className="menuGroup" key={section.title}>
              <h2>{section.title}</h2>
              <div className="grid">
                {section.items.map(([name, description, price]) => (
                  <article className="card" key={name}>
                    <div className="cardBody">
                      <h3>{name}</h3>
                      <p>{description}</p>
                      <span className="price">{price}</span>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
