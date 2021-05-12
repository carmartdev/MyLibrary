Array.prototype.names = function () {
    return this.map(({name}) => name).join(", ");
}

String.prototype.capitalize = function() {
    return this.replace(/\b\w/g, l => l.toUpperCase());
}

function bookTitle(title, authors) {
    if (title && authors) {
        return title.capitalize() + " by " + authors.names();
    }
}

function getCookie(name) {
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; ++i) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
}

function Header({itemsInCartCount}) {
    const cartCounter = itemsInCartCount ? " [" + itemsInCartCount + "]" : "";
    return (
        <header className="row align-items-center">
            <a className="col-auto text-body text-decoration-none"
               href="/">
                <h1>Bookstore</h1>
            </a>
            <form className="col input-group search-bar"
                  onSubmit={(e) => {
                      e.preventDefault()
                      window.location.hash = "/books/?" + new URLSearchParams({
                          search: e.target.search.value
                      });
                  }}>
                <input name="search"
                       type="text"
                       className="form-control"
                       aria-label="Search catalog" />
                <button className="btn search-btn input-group-text"
                        type="submit">
                    <svg xmlns="http://www.w3.org/2000/svg"
                         width="16"
                         height="16"
                         fill="currentColor"
                         className="bi bi-search"
                         viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"></path>
                    </svg>
                </button>
            </form>
            <div className="col-auto">
                <button type="button"
                        id="id-cart"
                        title="Shopping Cart"
                        className="text-uppercase fw-bold btn btn-outline-secondary"
                        data-bs-toggle="modal"
                        data-bs-target="#cart">
                    🛒 Cart{cartCounter}
                </button>
            </div>
        </header>
    );
}

function Body({books, cart, header, onCartChange}) {
    return (
        <div className="row">
            {header}
            <BookCatalog books={books}
                         cart={cart}
                         onCartChange={onCartChange} />
        </div>
    );
}

function AuthorsLinks(props) {
    const authors = props.authors.map((author, i) =>
        <React.Fragment key={author.key}>
            <a className="text-body text-decoration-none"
               data-bs-dismiss="modal"
               href={"#/books/?" + new URLSearchParams({author: author.key})}
               onClick={(e) => window.location = e.target.href}
               title={"Show more books by " + author.name}>
                   {author.name}
            </a>
            {i === props.authors.length - 1 ? "" : ", "}
        </React.Fragment>
    );
    return (<React.Fragment>{authors}</React.Fragment>)
}

function Cart({cart, onCartChange}) {
    const itemsInCart = cart.contents.map((book, i) =>
        <tr key={book.key} className="align-middle">
            <td>{i + 1}.</td>
            <td>
                <a className="text-body text-decoration-none"
                   href={"#/books/" + book.key + "/"}
                   onClick={(e) => window.location = e.target.href}
                   data-bs-dismiss="modal"
                   data-bs-toggle="modal"
                   data-bs-target="#bookDetails">
                        {book.title.capitalize()}
                </a>
            </td>
            <td><AuthorsLinks authors={book.authors} /></td>
            <td>${book.price}</td>
            <td>
                <input type="number"
                       onChange={(e) => fetch(
                            "/cart/update",
                            {
                                credentials: "include",
                                mode: "same-origin",
                                method: "POST",
                                headers: {
                                    "Accept": "application/json",
                                    "X-CSRFToken": getCookie("csrftoken"),
                                },
                                body: new URLSearchParams([[
                                    "qty " + book.key, e.target.value
                                ]])
                            }).then(response => onCartChange(),
                                    error => console.log(error))}
                       min="1"
                       size="4"
                       name={"qty " + book.key}
                       defaultValue={book.qty} />
            </td>
            <td>${book.total}</td>
            <td>
                <button className="btn-close" aria-label="Delete"
                        name="book_id"
                        onClick={() => fetch(
                            "/cart/delete",
                            {
                                credentials: "include",
                                mode: "same-origin",
                                method: "POST",
                                headers: {
                                    "Accept": "application/json",
                                    "X-CSRFToken": getCookie("csrftoken"),
                                },
                                body: new URLSearchParams({"book_id": book.key})
                            }).then(response => onCartChange(),
                                    error => console.log(error))} />
            </td>
        </tr>
    );
    if (itemsInCart.length) {
        return (
            <div className="modal fade"
                 id="cart"
                 tabIndex="-1"
                 aria-labelledby="cartLabel"
                 aria-hidden="true">
                <div className="modal-dialog modal-fullscreen">
                    <div className="modal-content"
                         style={{backgroundColor: "#fac68e",}}>
                        <div className="modal-header">
                            <h1 className="modal-title text-capitalize"
                                id="cartLabel">
                                Your Shopping Cart
                            </h1>
                            <button type="button"
                                    className="btn-close"
                                    data-bs-dismiss="modal"
                                    aria-label="Close">
                            </button>
                        </div>
                        <div className="modal-body">
                            <table id="id-book-catalog"
                                   className="table table-borderless table-striped">
                                <thead>
                                    <tr>
                                        <th>№</th>
                                        <th>Title</th>
                                        <th>Authors</th>
                                        <th>Price</th>
                                        <th>Qty</th>
                                        <th>Total</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {itemsInCart}
                                </tbody>
                                <thead>
                                <tr>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th></th>
                                    <th>Subtotal</th>
                                    <th id="id-total-price">${cart.total}</th>
                                    <th></th>
                                </tr>
                                </thead>
                            </table>
                        </div>
                        <div className="modal-footer">
                            <button type="button"
                                    id="id-checkout-button"
                                    className="btn btn-primary"
                                    data-bs-dismiss="modal"
                                    data-bs-toggle="modal"
                                    data-bs-target="#checkout">
                                checkout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="modal fade"
                 id="cart"
                 tabIndex="-1"
                 aria-labelledby="cartLabel"
                 aria-hidden="true">
                <div className="modal-dialog modal-fullscreen">
                    <div className="modal-content"
                         style={{backgroundColor: "#fac68e",}}>
                        <div className="modal-header">
                            <button type="button"
                                    className="btn-close"
                                    data-bs-dismiss="modal"
                                    aria-label="Close">
                            </button>
                        </div>
                        <div className="modal-body row align-items-center text-center">
                            <div>
                                <h3 className="my-3">
                                    Your Shopping Cart is empty
                                </h3>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button"
                                    className="btn btn-primary"
                                    data-bs-dismiss="modal">
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

function Checkout() {
    return (
        <div className="modal fade"
             id="checkout"
             tabIndex="-1"
             aria-labelledby="checkoutLabel"
             aria-hidden="true">
            <div className="modal-dialog modal-fullscreen">
                <div className="modal-content"
                     style={{backgroundColor: "#fac68e",}}>
                    <div className="modal-header">
                        <button type="button"
                                className="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close">
                        </button>
                    </div>
                    <div className="modal-body row align-items-center text-center">
                        <div>
                            <h1 className="my-3">
                                This is a demo store. You can't buy a real thing here.
                            </h1>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button"
                                className="btn btn-primary"
                                data-bs-dismiss="modal">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

function BookDetails({book: {title, cover, description, publisher,
                      publish_date, authors, isbn_10, isbn_13, price, key},
                     inCart, onCartChange}) {
    return (
        <div className="modal fade"
             id="bookDetails"
             tabIndex="-1"
             aria-labelledby="bookDetailsLabel"
             aria-hidden="true">
            <div className="modal-dialog modal-fullscreen">
                <div className="modal-content"
                     style={{backgroundColor: "#fac68e",}}>
                    <div className="modal-header">
                        <h1 className="modal-title text-capitalize"
                            id="bookDetailsLabel">
                            {title}
                        </h1>
                        <button type="button"
                                className="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close">
                        </button>
                    </div>
                    <div className="modal-body">
                        <div id="id-book-details"
                             className="info-window rounded">
                            <div className="row my-2">
                                <div className="col-auto mx-2 my-2">
                                    <img src={cover}
                                         className="rounded"
                                         alt={bookTitle(title, authors)} />
                                </div>
                                <div className="col">
                                    <h2><AuthorsLinks authors={authors} /></h2>
                                    <h4 className="py-3">{description}</h4>
                                    <p><b>Publisher:</b> {publisher}</p>
                                    <p><b>Publication date:</b> {publish_date}</p>
                                    <p><b>ISBN-10:</b> {isbn_10}</p>
                                    <p><b>ISBN-13:</b> {isbn_13}</p>
                                </div>
                                <div className="col-auto d-flex flex-column text-end">
                                    <h2 className="mx-2 my-2">${price}</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button"
                                className="btn btn-outline-secondary"
                                data-bs-dismiss="modal">
                            Close
                        </button>
                        <AddToCartButton bookId={key}
                                         inCart={inCart}
                                         onCartChange={onCartChange} />
                    </div>
                </div>
            </div>
        </div>
    );
}

function AddToCartButton({bookId, inCart, onCartChange}) {
    if (inCart) {
        return (
            <button type="button"
                    className="text-uppercase fw-bold btn btn-secondary"
                    data-bs-dismiss="modal"
                    data-bs-toggle="modal"
                    data-bs-target="#cart">
                in cart
            </button>
        )
    } else {
        return (
            <button type="button"
                    className="text-uppercase fw-bold btn btn-outline-secondary"
                    name="book_id"
                    onClick={() => fetch(
                        "/cart/add",
                        {
                            credentials: "include",
                            mode: "same-origin",
                            method: "POST",
                            headers: {
                                "Accept": "application/json",
                                "X-CSRFToken": getCookie("csrftoken"),
                            },
                            body: new URLSearchParams({"book_id": bookId})
                        }).then(response => onCartChange(),
                                error => console.log(error))} >
                add to cart
            </button>
        )
    }
}

function BookCart({book: {key, title, authors, cover, price}, cart,
                   onCartChange}) {
    return (
        <div className="card text-end mx-2 my-2 px-0 py-0">
            <a className="text-body text-decoration-none text-capitalize"
               href="#/"
               onClick={() => window.location.hash = "/books/" + key + "/"}
               data-bs-toggle="modal"
               data-bs-target="#bookDetails">
                    <img src={cover}
                         className="card-img-top"
                         alt={bookTitle(title, authors)}
                         title={bookTitle(title, authors)}/>
            </a>
            <div className="card-body d-flex flex-column">
                <p className="card-text fw-bold">${price}</p>
                <div>
                    <AddToCartButton bookId={key}
                                     inCart={cart.contents.map(({key}) => key)
                                             .includes(key)}
                                     onCartChange={onCartChange} />
                </div>
            </div>
        </div>
    );
}

function BookCatalog(props) {
    if (props.books.length) {
        return (
            <div id="id-book-catalog"
                 className="row justify-content-center info-window rounded">
                {props.books.map(book =>
                    <BookCart key={book.key}
                              cart={props.cart}
                              book={book}
                              onCartChange={props.onCartChange} />
                )}
            </div>
        );
    } else {
        return <p>No books are available.</p>
    }
}

function NavBar({pageLinks}) {
    const pages = pageLinks.map(([url, number, isActive, isBreak], i) => {
        return (
            <li key={url + i}
                className={"page-item" + (isActive ? " active" : "")}>
                <a className="page-link"
                   href={isBreak ? "#/" : "#" + url} >
                    {isBreak ? "..." : number}
                </a>
            </li>
        )
    })
    return (
        <nav className="row mx-2 my-2" aria-label="book catalog pages">
            <ul className="pagination justify-content-center">
                {pages}
            </ul>
        </nav>
    );
}

function Footer({pageLinks}) {
    return (
        <footer className="row py-3">
            <NavBar pageLinks={pageLinks} />
            <div className="col text-center">
                All books data is borrowed from&nbsp;
                <a href="https://openlibrary.org/">Open Library</a>;&nbsp;
                prices are generated randomly
            </div>
        </footer>
    );
}

class Root extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            catalogHeader: <React.Fragment />,
            book: {
                authors: [],
            },
            books: [],
            pageLinks: [],
            cart: {
                contents: [],
                total: 0,
            }
        };
        this.onHashChange = this.onHashChange.bind(this);
        this.updateCart = this.updateCart.bind(this);
        window.addEventListener("hashchange", this.onHashChange, false);
    }

    componentDidMount() {
        this.onHashChange();
        this.updateCart();
    }

    updateCart() {
        fetch("/cart/", {credentials: "include",
                         mode: "same-origin",
                         headers: {"Accept": "application/json"}})
            .then(response => response.json())
            .then(data => this.setState({cart: {contents: data.cart,
                                                total: data.total_price}}),
                  error => console.log(error))
    }

    onHashChange() {
        window.scrollTo(0, 0);
        const hash = window.location.hash.slice(1);
        if (/\/books\/\w*\//.test(hash)) {
            this.updateBookDetails(hash);
        } else {
            this.updateCatalog(hash);
        }
    }

    updateCatalog(url) {
        function header(response) {
            return (response.author
                        ? <h5>Books by {response.author}:</h5>
                        : response.keyword
                            ? <h5>Search results for "{response.keyword}":</h5>
                            : <React.Fragment />)
        }

        fetch(url, {headers: {"Accept": "application/json"}})
            .then(response => response.json())
            .then(response => this.setState({catalogHeader: header(response),
                                             books: response.results,
                                             pageLinks: response.page_links}),
                  error => console.log(error))
    }

    updateBookDetails(url) {
        window.history.pushState("", "", "/");
        fetch(url, {headers: {"Accept": "application/json"}})
            .then(response => response.json())
            .then(response => {this.setState({book: response})},
                  error => {console.log(error)})
    }

    render() {
        return (
            <React.Fragment>
                <BookDetails book={this.state.book}
                             inCart={this.state.cart.contents
                                     .map(({key}) => key)
                                     .includes(this.state.book.key)}
                             onCartChange={this.updateCart} />
                <Cart cart={this.state.cart}
                      onCartChange={this.updateCart} />
                <Checkout />
                <div className="container content">
                    <Header itemsInCartCount={this.state.cart.contents.length} />
                    <Body books={this.state.books}
                          cart={this.state.cart}
                          header={this.state.catalogHeader}
                          onCartChange={this.updateCart} />
                </div>
                <Footer pageLinks={this.state.pageLinks} />
            </React.Fragment>
        );
    }
}


// ========================================
let root = document.createElement("div");
root.classList.add("vh-100");
root.classList.add("d-flex");
root.classList.add("flex-column");
ReactDOM.render(<Root />, document.body.appendChild(root))
