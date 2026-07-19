import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Us",
  description: "Learn about FoodieHub, our mission and our commitment to fresh and delicious food."
};

export default function AboutPage() {
  return (
    <>
      <section className="pageHero">
        <div className="container">
          <h1>About FoodieHub</h1>
          <p>Good food brings people together.</p>
        </div>
      </section>
      <section className="section">
        <div className="container aboutGrid">
          <img
            src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80"
            alt="FoodieHub restaurant interior"
          />
          <div>
            <h2>Our Story</h2>
            <p>FoodieHub was created with one simple goal: to serve fresh, tasty and affordable food in a welcoming environment.</p>
            <p>Our chefs prepare every dish with quality ingredients, traditional flavours and modern presentation.</p>
            <h3>Our Mission</h3>
            <p>To make every meal enjoyable through good taste, friendly service and consistent quality.</p>
          </div>
        </div>
      </section>
    </>
  );
}
