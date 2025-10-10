function CodeBlock() return {} end  -- Ignore code blocks
function Code() return {} end       -- Ignore inline code

function Doc(body, meta)
    local str = pandoc.utils.stringify(body)
    local wordcount = #pandoc.utils.words(str)
    print("Word count (excluding code): " .. wordcount)
    return nil
end