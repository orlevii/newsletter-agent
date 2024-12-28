# Newsletter Agent
AI Agent for finding relevant articles and summarizing them.

## Configuration

* Create an empty directory
* Create a `config.yaml`, use the following reference:
```yaml
$schema: "https://raw.githubusercontent.com/orlevii/newsletter-agent/refs/heads/main/config_schema.json"
guidelines:
  relevance: |
    * The article is about LLMs
    * The article is about big AI companies like OpenAI, Anthropic, Google, Meta, etc...
    * The article is about fundraising or acquisitions in the AI space
    * The article is about prompt evaluations

    ## Example 1
    Input:
    Perplexity's Carbon integration will make it easier for enterprises to connect their data to AI search

    Output:
    {
      "reason": "The article is Perplexity's Carbon integration, that means the article does not meet the criteria",
      "is_relevant": false
    }

  summarization: |
    * Use bullets

sources:
  - name: Venturebeat
    url: "https://venturebeat.com/category/ai/"
  - name: Techcrunch
    url: "https://techcrunch.com/category/artificial-intelligence/"
  - name: Huggingface Blog
    url: "https://huggingface.co/blog"
```

## Running

```bash
docker run --rm -it \
  -v $(pwd):/data \
  -e OPENAI_API_KEY=<YOUR_API_KEY> \
  orlevi/newsletter-agent:latest
```
Or with `.env` file:
```bash
docker run --rm -it \
  -v $(pwd):/data \
  --env-file .env \
  orlevi/newsletter-agent:latest
```