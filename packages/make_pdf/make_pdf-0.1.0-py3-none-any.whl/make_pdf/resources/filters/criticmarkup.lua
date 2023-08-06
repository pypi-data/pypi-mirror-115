-- Enable Criticmarkup
function RawInline(el)
  return processBlockOrInline(el, false)
end

function RawBlock(el)
  return processBlockOrInline(el, true)
end

function processBlockOrInline(el, block)
  -- Replace HTML-Comments with latex-comments
  if is_html(el.format) and (string.starts(el.text, "<!--")) then
    newText = "\\chcomment{" .. string.gsub(string.gsub(el.text, "<!%-%-% ", ""), "%-%->", "") .. "}" 
    if block then
      return pandoc.RawBlock("tex", newText)
    end
    return pandoc.RawInline("tex", newText)
  end
  -- Replace preprocessed changes-tags with prefixed changes-tags
  if is_tex(el.format) and (string.starts(el.text,"\\added") or string.starts(el.text,"\\deleted") or string.starts(el.text, "\\replaced") or string.starts(el.text, "\\highlight") or string.starts(el.text, "\\comment")) then
    newText = string.gsub(el.text, "\\", "\\ch", 1)
    if block then
      return pandoc.RawBlock("tex", newText)
    end
    return pandoc.RawInline("tex", newText)
  end
  return el
end

function is_tex(format)
    return format == 'latex' or format == 'tex' or format == 'context'
end

function is_html (format)
    return format == 'html' or format == 'html4' or format == 'html5'
end

function string.starts(fullString,substring)
   return string.sub(fullString,1,string.len(substring))==substring
end
