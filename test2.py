from taipy.gui import Gui


content = ""
img_path = "input.png"
prob = 0
pred = ""

index = """
<|text-center|
<|{"input.png"}|image|width=25vw|>

<|{content}|file_selector|extensions=.png|>
select an image from your file system

<|{pred}|>

<|{img_path}|image|>

<|{prob}|indicator|value={prob}|min=0|max=100|width=25vw|>
>
"""


def on_change(state, var_name, var_val):
    if var_name == "content":
        # top_prob, top_pred = predict_image(model, var_val)
        top_prob, top_pred = 0.1, 'hello'
        state.prob = round(top_prob * 100)
        state.pred = "this is a " + top_pred
        state.img_path = var_val


app = Gui(page=index)

if __name__ == "__main__":
    app.run(use_reloader=True,title="TAIPY demo")