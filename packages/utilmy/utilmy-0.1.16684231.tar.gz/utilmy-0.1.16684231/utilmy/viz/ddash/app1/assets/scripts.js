const PATH = {
    'links':'about:blank',
    'html':'assets/html/',
    'dash':'pages/'
}

const html = 'html'
const NUMERIC = new RegExp(/^[0-9]*$/)
const VALID_LINKS = new RegExp('^(http[s]?:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_\+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?')

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render: function(targetRender, homePage) {
            if (targetRender.length == 0){

                if (VALID_LINKS.test(homePage)){
                    return homePage
                } else if (homePage.endsWith(html)) {
                    return `${PATH[html]}${homePage}` 
                } else if (homePage.endsWith('.py')) {
                    return `${PATH['dash']}${homePage}`
                }
            } else {
                let target = targetRender[0]
                if (!NUMERIC.test(target)){
    
                    if (VALID_LINKS.test(target)){
                        return target 
                    } else if (target.endsWith(html)){
                        return `${PATH[html]}${target}`
                    } else if (target.endsWith('.py')) {
                        return `${PATH['dash']}${target}`
                    }
    
                }

            }

            return dash_clientside.no_update 
            
        }
    }
});