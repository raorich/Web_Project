# Luxury Auction Web Platform

## Project Overview
This project is a web platform for auctioning luxury items, focusing on three main categories: **classic cars, high-end watches, and fine art**. Users can register as buyers or sellers, manage stores, place bids, and track acquisition history.  

The platform uses **Django** as backend, with a **PostgreSQL/SQLite database** and front-end styled using **HTML, Tailwind CSS, and JavaScript**.

---

## Features
- User authentication & registration  
- Admin interface for managing products, stores, and users  
- Product listings for cars, watches, and art  
- Bidding system with acquisition and sales history  
- Data scraping (Selenium) for watch products  
- RDFa semantic markup for SEO (ProductModel, VisualArtwork, Vehicle)  

---

## Database Model
The database includes the following main entities:

| Entity | Description |
|--------|-------------|
| User | Buyers and sellers, acquisition history, N-M relationship with products and bids |
| Store | Contains multiple products, associated with multiple users (1-N relationship with products) |
| Product | Luxury items, receives multiple bids, unique to a store |
| Bid | Intermediate table between User and Product, tracks bid amount and timestamp |
| AcquisitionHistory | Records completed purchases |
| SalesHistory | Records product sales by store |

**Product Models:**  

- **Car:** brand, model, year, category, mileage, fuel type, transmission, horsepower, color, price, image  
- **Watch:** brand, model, year, category, condition, materials, estimated value, image  
- **Art:** name, artist, category, year, medium, dimensions, estimated value, image  

---

## Architecture
- **Backend:** Django, Python  
- **Frontend:** HTML, Tailwind CSS, JS  
- **Database:** PostgreSQL / SQLite  
- **Scraping:** Selenium for automatic watch product import  
- **Structured Data:** RDFa in product detail page for SEO (Schema.org: ProductModel, VisualArtwork, Vehicle)  

---

## Installation & Running the Project
1. Clone the repository:  
```bash
git clone <repository-url>
cd <repo-folder>
```

2. Create a virtual environment and install dependencies:  
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Apply migrations:  
```bash
python manage.py migrate
```

4. Create a superuser (optional, for admin interface):  
```bash
python manage.py createsuperuser
```

5. Run the development server:  
```bash
python manage.py runserver
```

6. Open your browser:  
```
http://127.0.0.1:8000
```

---

## Screenshots / Visuals
*(Add images in a `/docs` folder and reference them here, e.g.,)*

```markdown
![Home Page](./docs/homepage.png)
![Product Detail](./docs/product_detail.png)
```

---

## Technical Decisions
- **Store-Product Relationship:** 1-N instead of N-N to ensure uniqueness  
- **Bid Model:** Intermediate model with ForeignKeys to capture bid history  
- **RDFa Markup:** For SEO and semantic web compliance  
