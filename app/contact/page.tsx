import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact",
  description: "Contact FoodieHub for restaurant details, table bookings and food enquiries."
};

export default function ContactPage() {
  return (
    <>
      <section className="pageHero">
        <div className="container">
          <h1>Contact Us</h1>
          <p>We would love to hear from you.</p>
        </div>
      </section>
      <section className="section">
        <div className="container contactGrid">
          <div>
            <h2>Visit FoodieHub</h2>
            <p><strong>Address:</strong><br />Madhapur, Hyderabad, Telangana</p>
            <p><strong>Phone:</strong><br />+91 98765 43210</p>
            <p><strong>Email:</strong><br />hello@foodiehub.com</p>
            <p><strong>Business Hours:</strong><br />Monday – Sunday: 11:00 AM – 11:00 PM</p>
          </div>
          <form className="form">
            <input className="input" type="text" placeholder="Your name" aria-label="Your name" />
            <input className="input" type="email" placeholder="Your email" aria-label="Your email" />
            <input className="input" type="tel" placeholder="Mobile number" aria-label="Mobile number" />
            <textarea placeholder="Your message" aria-label="Your message"></textarea>
            <button className="btn" type="button">Send Message</button>
          </form>
        </div>
      </section>
    </>
  );
}
