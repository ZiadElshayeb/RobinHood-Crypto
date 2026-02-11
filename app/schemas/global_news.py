from pydantic import BaseModel, Field
from typing import Optional

class GlobalNewsRequest(BaseModel):
    action: str = Field(default="getArticles", description="The action to perform.")
    apiKey: str = Field(description="Your API key for authentication.", examples=["YOUR_API_KEY"])
    
    resultType: str = Field(default="articles", description="Define what kind of results to return.")
    articlesPage: int = Field(default=1, description="Page number of results (starting from 1).")
    articlesCount: int = Field(default=100, description="Number of articles to return (max 100).")
    articlesSortBy: str = Field(default="date", description="Criteria for sorting articles.")
    articlesSortByAsc: bool = Field(default=False, description="Sort in ascending order.")
    articleBodyLen: int = Field(default=-1, description="Size of article body (-1 for full body).")
    
    dataType: list[str] | str = Field(default=["news"], description="Data types to search: news, pr, blog.")
    forceMaxDataTimeWindow: Optional[int] = Field(default=None, description="Max age of content in days (7 or 31).")
    
    keyword: Optional[str | list[str]] = Field(default=None, description="Keyword or phrase to search.")
    lang: Optional[str | list[str]] = Field(default=None, description="Language codes (ISO3).")
    
    dateStart: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD).")
    dateEnd: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD).")
    dateMentionStart: Optional[str] = Field(default=None, description="Start date mentioned in article (YYYY-MM-DD).")
    dateMentionEnd: Optional[str] = Field(default=None, description="End date mentioned in article (YYYY-MM-DD).")
    
    keywordLoc: str = Field(default="body", description="Where to search keywords: body, title, or body,title.")
    keywordOper: str = Field(default="and", description="Boolean operator for keywords: and or or.")
        
    startSourceRankPercentile: int = Field(default=0, description="Start ranking percentile (0-90).")
    endSourceRankPercentile: int = Field(default=100, description="End ranking percentile (10-100).")
    minSentiment: Optional[float] = Field(default=None, description="Minimum sentiment (-1 to 1).")
    maxSentiment: Optional[float] = Field(default=None, description="Maximum sentiment (-1 to 1).")
        
    includeArticleTitle: bool = Field(default=True, description="Include article title.")
    includeArticleBasicInfo: bool = Field(default=True, description="Include core article info.")
    includeArticleBody: bool = Field(default=True, description="Include article body.")
    includeArticleSentiment: bool = Field(default=True, description="Include sentiment.")
    includeArticleLocation: bool = Field(default=False, description="Include location.")
    includeArticleExtractedDates: bool = Field(default=False, description="Include extracted dates.")
    includeSourceTitle: bool = Field(default=True, description="Include source title.")

class GlobalNewsSource(BaseModel):
    uri: str = Field(description="Source URI.")
    dataType: str = Field(description="Data type.")
    title: str = Field(description="Source title.")

class GlobalNewsConceptLabel(BaseModel):
    eng: str = Field(description="English label.")

class GlobalNewsLocation(BaseModel):
    type: str = Field(description="Location type.")
    label: GlobalNewsConceptLabel = Field(description="Location label.")
    country: Optional[dict] = Field(default=None, description="Country information.")

class GlobalNewsConcept(BaseModel):
    uri: str = Field(description="Concept URI.")
    type: str = Field(description="Concept type.")
    score: int = Field(description="Relevance score.")
    label: GlobalNewsConceptLabel = Field(description="Concept label.")
    location: Optional[GlobalNewsLocation] = Field(default=None, description="Location if applicable.")

class GlobalNewsArticle(BaseModel):
    uri: str = Field(description="Article URI.")
    lang: str = Field(description="Article language.")
    isDuplicate: bool = Field(description="Is duplicate article.")
    date: str = Field(description="Publication date.")
    time: str = Field(description="Publication time.")
    dateTime: str = Field(description="Publication datetime.")
    dateTimePub: str = Field(description="Publication datetime with timezone.")
    dataType: str = Field(description="Data type.")
    sim: float = Field(description="Similarity score.")
    title: str = Field(description="Article title.")
    body: str = Field(description="Article body.")
    source: GlobalNewsSource = Field(description="Article source.")
    concepts: Optional[list[GlobalNewsConcept]] = Field(default=None, description="Article concepts.")
    sentiment: Optional[float] = Field(default=None, description="Article sentiment.")
    wgt: int = Field(description="Weight score.")
    relevance: int = Field(description="Relevance score.")

class GlobalNewsArticlesResult(BaseModel):
    results: list[GlobalNewsArticle] = Field(description="List of articles.")
    totalResults: int = Field(description="Total number of results.")
    page: int = Field(description="Current page number.")
    count: int = Field(description="Number of results in current page.")
    pages: int = Field(description="Total number of pages.")

class GlobalNewsResponse(BaseModel):
    articles: GlobalNewsArticlesResult = Field(description="Articles result.")
