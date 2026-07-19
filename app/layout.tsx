import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "FoodieHub | Fresh Food, Happy Moments",
    template: "%s | FoodieHub"
  },
  description: "FoodieHub serves fresh, tasty and affordable dishes including biryani, pizza, burgers, desserts and beverages.",
  keywords: ["food restaurant", "biryani", "pizza", "burgers", "desserts", "FoodieHub"]
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header className="header">
          <div className="container nav">
            <Link className="logo" href="/">🍽️ FoodieHub</Link>
            <nav className="navLinks" aria-label="Main navigation">
              <Link href="/">Home</Link>
              <Link href="/menu">Menu</Link>
              <Link href="/about">About</Link>
              <Link href="/contact">Contact</Link>
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="footer">
          <div className="container">
            <div className="footerGrid">
              <div>
                <h3>🍽️ FoodieHub</h3>
                <p>Fresh ingredients, delicious food and friendly service for every customer.</p>
              </div>
              <div>
                <h3>Quick Links</h3>
                <p><Link href="/menu">Menu</Link></p>
                <p><Link href="/about">About Us</Link></p>
                <p><Link href="/contact">Contact</Link></p>
              </div>
              <div>
                <h3>Contact</h3>
                <p>📞 +91 98765 43210</p>
                <p>✉️ hello@foodiehub.com</p>
                <p>📍 Hyderabad, Telangana</p>
              </div>
            </div>
            <div className="copyright">© 2026 FoodieHub. All rights reserved.</div>
          </div>
        </footer>
      </body>
    </html>
  );
}
