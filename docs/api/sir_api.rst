API Documentation
*****************

.. raw:: html

      <script src="./sir_api_files/highlight.pack.js"></script>

      <script>hljs.initHighlightingOnLoad();</script>

      You can interact with the agent using a RESTful API. This API gives you full access to the agent and its data.

      <h4 class="endpoint_documentation">Variables</h4>

      When reading this documentation you will find variables in two forms:

      <ul>
        <li class="argument_element"><em class="argument">&lt;variable&gt;:</em> Variables that are between &lt;&gt; have to be replaced by their values in the URL. For example, <code>/api/v1.0/variables/categories/&lt;category&gt;</code> will turn into <code>/api/v1.0/variables/categories/my_category</code>.</li>
        <li class="argument_element"><em class="argument">variable:</em> Variables that are NOT enclosed by &lt;&gt;:
          <ul>
            <li class="argument_element">If the method is a GET variables that are between &lt;&gt; have to be replaced by their values in the URL. For example, <code>/api/v1.0/variables/categories/&lt;category&gt;</code> will turn into <code>/api/v1.0/variables/categories/my_category</code>.</li>
            <li class="argument_element">If the method is a POST or a PUT variables variables that are between &lt;&gt; have to sent as a JSON object.</li>
          </ul></li>
      </ul>

      <h4 class="endpoint_documentation">Responses</h4>

      All the responses from the agent will be in JSON format and will include three sections:

      <ul>
        <li><em>meta</em>: Metainformation about the response. For example, request_time, length of the response or if there was any error.</li>
        <li><em>parameters</em>: The parameters used for the call.</li>
        <li><em>result</em>: The result of the call or a description of the error if there was any.</li>
      </ul>

      For example, for the following call you will get the following response:

      <pre><code class="hljs">/api/v1.0/analytics/top_prefixes?limit_prefixes=10&amp;start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00&amp;net_masks=20,24</code></pre>
      <pre><code class="json hljs">
        {
          "<span class="hljs-attribute">meta</span>": <span class="hljs-value">{
            "<span class="hljs-attribute">error</span>": <span class="hljs-value"><span class="hljs-literal">false</span></span>,
            "<span class="hljs-attribute">length</span>": <span class="hljs-value"><span class="hljs-number">10</span></span>,
            "<span class="hljs-attribute">request_time</span>": <span class="hljs-value"><span class="hljs-number">11.99163</span>
          </span>}</span>,
          "<span class="hljs-attribute">parameters</span>": <span class="hljs-value">{
            "<span class="hljs-attribute">end_time</span>": <span class="hljs-value"><span class="hljs-string">"2015-07-14T14:00"</span></span>,
            "<span class="hljs-attribute">exclude_net_masks</span>": <span class="hljs-value"><span class="hljs-literal">false</span></span>,
            "<span class="hljs-attribute">limit_prefixes</span>": <span class="hljs-value"><span class="hljs-number">10</span></span>,
            "<span class="hljs-attribute">net_masks</span>": <span class="hljs-value"><span class="hljs-string">"20,24"</span></span>,
            "<span class="hljs-attribute">start_time</span>": <span class="hljs-value"><span class="hljs-string">"2015-07-13T14:00"</span>
          </span>}</span>,
          "<span class="hljs-attribute">result</span>": <span class="hljs-value">[
            {
              "<span class="hljs-attribute">as_dst</span>": <span class="hljs-value"><span class="hljs-number">43650</span></span>,
              "<span class="hljs-attribute">key</span>": <span class="hljs-value"><span class="hljs-string">"194.14.177.0/24"</span></span>,
              "<span class="hljs-attribute">sum_bytes</span>": <span class="hljs-value"><span class="hljs-number">650537594</span>
            </span>},
            ...
            {
              "<span class="hljs-attribute">as_dst</span>": <span class="hljs-value"><span class="hljs-number">197301</span></span>,
              "<span class="hljs-attribute">key</span>": <span class="hljs-value"><span class="hljs-string">"80.71.128.0/20"</span></span>,
              "<span class="hljs-attribute">sum_bytes</span>": <span class="hljs-value"><span class="hljs-number">5106731</span>
            </span>}
          ]
        </span>}</code></pre>



      <h3 class="title">Analytics Endpoint</h3>


      <h4 class="endpoint_documentation">/api/v1.0/analytics/top_prefixes</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves TOP prefixes sorted by the amount of bytes that they consumed during the specified period of time.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">exclude_net_masks:</em> Optional. If set to any value it will return prefixes with a prefix length not included in net_masks. If set to 0 it will return only prefixes with a prefix length included in net_masks. Default is 0.
          </li>

          <li class="argument_element"><em class="argument">limit_prefixes:</em> Optional. Number of top prefixes to retrieve.
          </li>

          <li class="argument_element"><em class="argument">start_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Starting time of the range.
          </li>

          <li class="argument_element"><em class="argument">net_masks:</em> Optional. List of prefix lengths to filter in or out.
          </li>

          <li class="argument_element"><em class="argument">end_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Ending time of the range.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of prefixes sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&amp;start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00
          </li>

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&amp;start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00&amp;net_masks=20,24
          </li>

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/analytics/top_prefixes?limit_prefixes=10&amp;start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00&amp;net_masks=20,24&amp;exclude_net_masks=1
          </li>

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/analytics/top_asns</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves TOP ASN's sorted by the amount of bytes that they consumed during the specified period of time.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">start_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Starting time of the range.
          </li>

          <li class="argument_element"><em class="argument">end_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Ending time of the range.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of ASN's sorted by sum_bytes. The attribute sum_bytes is the amount of bytes consumed during the specified time.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/analytics/top_asns?start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00
          </li>

      </ul>









      <h3 class="title">Variables Endpoint</h3>


      <h4 class="endpoint_documentation">/api/v1.0/variables</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the variables in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of all the variables.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables
          </li>

      </ul>



      <h5 class="endpoint_documentation">POST</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      You can create a variable from the CLI with curl like this: <pre><code class="hljs python">curl -i -H <span class="hljs-string">"Content-Type: application/json"</span> -X POST -d <span class="hljs-string">'{"name": "test_var", "content": "whatever", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}'</span> http://<span class="hljs-number">127.0</span>.0.1:<span class="hljs-number">5000</span>/api/v1.0/variables</code></pre>

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">content:</em> Content of the variable.
          </li>

          <li class="argument_element"><em class="argument">category:</em> Category of the variable.
          </li>

          <li class="argument_element"><em class="argument">name:</em> Name of the variable.
          </li>

          <li class="argument_element"><em class="argument">extra_vars:</em> Use this field to add extra data to your variable. It is recommended to use a JSON string
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">The variable that was just created</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/variables/categories</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the categories in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of all the categories.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables/categories
          </li>

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/variables/categories/&lt;category&gt;</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the variables the belong to &lt;category&gt; in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">&lt;category&gt;:</em> Category you want to query
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of variables belonging to &lt;category&gt;.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables/categories/&lt;category&gt;
          </li>

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/variables/categories/&lt;category&gt;/&lt;name&gt;</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves the variable with &lt;name&gt; and &lt;category&gt;.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">&lt;category&gt;:</em> Category of the variable you want to retrieve.
          </li>

          <li class="argument_element"><em class="argument">&lt;name&gt;:</em> Name of the variable you want to retrieve.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of variables belonging to &lt;category&gt;.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables/categories/&lt;category&gt;/&lt;name&gt;
          </li>

      </ul>



      <h5 class="endpoint_documentation">PUT</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      This API call allows you to modify all of some of the values of a variable. For example, you can update the <em>name</em> and the <em>extra_vars</em> of a variable with the following command: <pre><code class="hljs python"> curl -i -H <span class="hljs-string">"Content-Type: application/json"</span> -X PUT -d <span class="hljs-string">'{"name": "test_varc", "extra_vars": "{'</span>my_param1<span class="hljs-string">': '</span>my_value1<span class="hljs-string">', '</span>my_param2<span class="hljs-string">': '</span>my_value2<span class="hljs-string">'}"}'</span> http://<span class="hljs-number">127.0</span>.0.1:<span class="hljs-number">5000</span>/api/v1.0/variables/categories/development/test_vara HTTP/<span class="hljs-number">1.0</span> <span class="hljs-number">200</span> OK Content-Type: application/json Content-Length: <span class="hljs-number">358</span> Server: Werkzeug/<span class="hljs-number">0.10</span>.4 Python/<span class="hljs-number">2.7</span>.8 Date: Tue, <span class="hljs-number">21</span> Jul <span class="hljs-number">2015</span> <span class="hljs-number">10</span>:<span class="hljs-number">16</span>:<span class="hljs-number">22</span> GMT
      {
        <span class="hljs-string">"meta"</span>: {
          <span class="hljs-string">"error"</span>: false,
          <span class="hljs-string">"length"</span>: <span class="hljs-number">1</span>,
          <span class="hljs-string">"request_time"</span>: <span class="hljs-number">0.0055</span>
        },
        <span class="hljs-string">"parameters"</span>: {
          <span class="hljs-string">"categories"</span>: <span class="hljs-string">"development"</span>,
          <span class="hljs-string">"name"</span>: <span class="hljs-string">"test_vara"</span>
        },
        <span class="hljs-string">"result"</span>: [
          {
            <span class="hljs-string">"category"</span>: <span class="hljs-string">"development"</span>,
            <span class="hljs-string">"content"</span>: <span class="hljs-string">"whatever"</span>,
            <span class="hljs-string">"extra_vars"</span>: <span class="hljs-string">"{my_param1: my_value1, my_param2: my_value2}"</span>,
            <span class="hljs-string">"name"</span>: <span class="hljs-string">"test_varc"</span>
          }
        ]
        }
        </code></pre>

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">category:</em> Optional. New category.
          </li>

          <li class="argument_element"><em class="argument">content:</em> Optional. New content.
          </li>

          <li class="argument_element"><em class="argument">name:</em> Optional. New name.
          </li>

          <li class="argument_element"><em class="argument">&lt;name&gt;:</em> Name of the variable you want to modify.
          </li>

          <li class="argument_element"><em class="argument">&lt;category&gt;:</em> Category of the variable you want to modify.
          </li>

          <li class="argument_element"><em class="argument">extra_vars:</em> Optional. New extra_vars.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">The variable with the new data.</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables/categories/&lt;category&gt;/&lt;name&gt;
          </li>

      </ul>



      <h5 class="endpoint_documentation">DELETE</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Deletes a variable. For example: <pre><code class="hljs python"> curl -i -X DELETE http://<span class="hljs-number">127.0</span>.0.1:<span class="hljs-number">5000</span>/api/v1.0/variables/categories/deveopment/test_vara HTTP/<span class="hljs-number">1.0</span> <span class="hljs-number">200</span> OK Content-Type: application/json Content-Length: <span class="hljs-number">183</span> Server: Werkzeug/<span class="hljs-number">0.10</span>.4 Python/<span class="hljs-number">2.7</span>.8 Date: Tue, <span class="hljs-number">21</span> Jul <span class="hljs-number">2015</span> <span class="hljs-number">10</span>:<span class="hljs-number">17</span>:<span class="hljs-number">27</span> GMT
      {
        <span class="hljs-string">"meta"</span>: {
          <span class="hljs-string">"error"</span>: false,
          <span class="hljs-string">"length"</span>: <span class="hljs-number">0</span>,
          <span class="hljs-string">"request_time"</span>: <span class="hljs-number">0.0016</span>
        },
        <span class="hljs-string">"parameters"</span>: {
          <span class="hljs-string">"categories"</span>: <span class="hljs-string">"deveopment"</span>,
          <span class="hljs-string">"name"</span>: <span class="hljs-string">"test_vara"</span>
        },
        <span class="hljs-string">"result"</span>: []
      } </code></pre>

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">&lt;category&gt;:</em> Category of the variable you want to delete.
          </li>

          <li class="argument_element"><em class="argument">&lt;name&gt;:</em> Name of the variable you want to delete.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">An empty list</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/variables/categories/&lt;category&gt;/&lt;name&gt;
          </li>

      </ul>









      <h3 class="title">Pmacct Endpoint</h3>


      <h4 class="endpoint_documentation">/api/v1.0/pmacct/dates</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the available dates in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of all the available dates in the system</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/pmacct/dates
          </li>

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/pmacct/flows</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the available dates in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">start_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Starting time of the range.
          </li>

          <li class="argument_element"><em class="argument">end_time:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'. Ending time of the range.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of all the available dates in the system</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&amp;start_time=2015-07-14T14:00&amp;end_time=2015-07-14T14:01
          </li>

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/pmacct/flows?limit_prefixes=10&amp;start_time=2015-07-13T14:00&amp;end_time=2015-07-14T14:00
          </li>

      </ul>





      <h4 class="endpoint_documentation">/api/v1.0/pmacct/bgp_prefixes</h4>


      <h5 class="endpoint_documentation">GET</h5>

      <em class="endpoint_documentation">Description:</em>

      <div class="endpoint_documentation">
      Retrieves all the BGP prefixes in the system.

      </div>

      <em class="endpoint_documentation">Arguments:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element"><em class="argument">date:</em> Mandatory. Datetime in unicode string following the format '%Y-%m-%dT%H:%M:%S'.
          </li>

      </ul>

      <em class="endpoint_documentation">Returns:</em>
      <ul class="endpoint_documentation">
          <li class="argument_element">A list of all the available BGP prefixes in the system</li>
      </ul>

      <em class="endpoint_documentation">Examples:</em>
      <ul class="endpoint_documentation">

          <li class="argument_element">http://127.0.0.1:5000/api/v1.0/pmacct/bgp_prefixes?date=2015-07-16T11:00:01
          </li>

      </ul>
