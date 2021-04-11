function Root(props) {
    return (
        <div class="row vh-100 align-items-center text-center">
            <h1>You need to <b>disable</b> JavaScript to run this app.</h1>
        </div>
    );
};

// ========================================

ReactDOM.render(
    <Root />,
    document.body.appendChild(document.createElement("div"))
)
