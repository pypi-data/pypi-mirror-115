-- Set the current date if the date of the document is nil
function Meta(m)
  if m.date == nil then
    -- since lua seems to override the set locale for everything but ctype, we manually set the locale into time.
    os.setlocale(os.setlocale(nil, "ctype"), "time")
    if string.starts(os.setlocale(nil, "ctype"), "en") or os.setlocale(nil, "ctype") == "C" then
      m.date = os.date("%e of %B %Y")
    elseif string.starts(os.setlocale(nil, "ctype"), "de") then
      m.date = os.date("%e. %B %Y")
    end
    return m
  end
end

function string.starts(fullString,substring)
   return string.sub(fullString,1,string.len(substring))==substring
end
