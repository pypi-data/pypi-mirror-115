-- convert all fences into latex-environments ending in "Box". 
function Div(el)
  fenceName = el.classes[1]
  title = el.attributes["title"]
  if title == nil then
    title = ""
  end
  -- insert element in front
  table.insert(
    el.content, 1,
    pandoc.RawBlock("latex", "\\begin{" .. fenceName .. "Box}{" .. title .. "}"))
  -- insert element at the back
  table.insert(
    el.content,
    pandoc.RawBlock("latex", "\\end{" .. fenceName .. "Box}"))
  return el
end
