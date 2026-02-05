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
    conceptUri: Optional[str | list[str]] = Field(default=None, description="Concept URI to search.")
    categoryUri: Optional[str | list[str]] = Field(default=None, description="Category URI to search.")
    sourceUri: Optional[str | list[str]] = Field(default=None, description="News source URI.")
    sourceLocationUri: Optional[str | list[str]] = Field(default=None, description="Source location URI.")
    sourceGroupUri: Optional[str | list[str]] = Field(default=None, description="Source group URI.")
    authorUri: Optional[str | list[str]] = Field(default=None, description="Author URI.")
    locationUri: Optional[str | list[str]] = Field(default=None, description="Location URI mentioned in dateline.")
    lang: Optional[str | list[str]] = Field(default=None, description="Language codes (ISO3).")
    
    dateStart: Optional[str] = Field(default=None, description="Start date (YYYY-MM-DD).")
    dateEnd: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD).")
    dateMentionStart: Optional[str] = Field(default=None, description="Start date mentioned in article (YYYY-MM-DD).")
    dateMentionEnd: Optional[str] = Field(default=None, description="End date mentioned in article (YYYY-MM-DD).")
    
    keywordLoc: str = Field(default="body", description="Where to search keywords: body, title, or body,title.")
    keywordOper: str = Field(default="and", description="Boolean operator for keywords: and or or.")
    conceptOper: str = Field(default="and", description="Boolean operator for concepts: and or or.")
    categoryOper: str = Field(default="or", description="Boolean operator for categories: and or or.")
    
    ignoreKeyword: Optional[str | list[str]] = Field(default=None, description="Keywords to ignore.")
    ignoreConceptUri: Optional[str | list[str]] = Field(default=None, description="Concept URIs to ignore.")
    ignoreCategoryUri: Optional[str | list[str]] = Field(default=None, description="Category URIs to ignore.")
    ignoreSourceUri: Optional[str | list[str]] = Field(default=None, description="Source URIs to ignore.")
    ignoreSourceLocationUri: Optional[str | list[str]] = Field(default=None, description="Source locations to ignore.")
    ignoreSourceGroupUri: Optional[str | list[str]] = Field(default=None, description="Source groups to ignore.")
    ignoreLocationUri: Optional[str | list[str]] = Field(default=None, description="Locations to ignore.")
    ignoreAuthorUri: Optional[str | list[str]] = Field(default=None, description="Authors to ignore.")
    ignoreLang: Optional[str | list[str]] = Field(default=None, description="Languages to ignore.")
    ignoreKeywordLoc: str = Field(default="body", description="Where to search ignore keywords.")
    
    startSourceRankPercentile: int = Field(default=0, description="Start ranking percentile (0-90).")
    endSourceRankPercentile: int = Field(default=100, description="End ranking percentile (10-100).")
    minSentiment: Optional[float] = Field(default=None, description="Minimum sentiment (-1 to 1).")
    maxSentiment: Optional[float] = Field(default=None, description="Maximum sentiment (-1 to 1).")
    
    isDuplicateFilter: str = Field(default="keepAll", description="Duplicate filter: skipDuplicates, keepOnlyDuplicates, keepAll.")
    eventFilter: str = Field(default="keepAll", description="Event filter: skipArticlesWithoutEvent, keepOnlyArticlesWithoutEvent, keepAll.")
    
    includeArticleTitle: bool = Field(default=True, description="Include article title.")
    includeArticleBasicInfo: bool = Field(default=True, description="Include core article info.")
    includeArticleBody: bool = Field(default=True, description="Include article body.")
    includeArticleEventUri: bool = Field(default=True, description="Include event URI.")
    includeArticleSocialScore: bool = Field(default=False, description="Include social media shares.")
    includeArticleSentiment: bool = Field(default=True, description="Include sentiment.")
    includeArticleConcepts: bool = Field(default=False, description="Include concepts.")
    includeArticleCategories: bool = Field(default=False, description="Include categories.")
    includeArticleLocation: bool = Field(default=False, description="Include location.")
    includeArticleImage: bool = Field(default=True, description="Include image.")
    includeArticleAuthors: bool = Field(default=True, description="Include authors.")
    includeArticleVideos: bool = Field(default=False, description="Include videos.")
    includeArticleLinks: bool = Field(default=False, description="Include links.")
    includeArticleExtractedDates: bool = Field(default=False, description="Include extracted dates.")
    includeArticleDuplicateList: bool = Field(default=False, description="Include duplicate list.")
    includeArticleOriginalArticle: bool = Field(default=False, description="Include original article.")
    includeSourceTitle: bool = Field(default=True, description="Include source title.")
    includeSourceDescription: bool = Field(default=False, description="Include source description.")
    includeSourceLocation: bool = Field(default=False, description="Include source location.")
    includeSourceRanking: bool = Field(default=False, description="Include source ranking.")
    includeConceptLabel: bool = Field(default=True, description="Include concept label.")
    includeConceptImage: bool = Field(default=False, description="Include concept image.")
    includeConceptSynonyms: bool = Field(default=False, description="Include concept synonyms.")
    conceptLang: str = Field(default="eng", description="Language of concept label.")
    includeCategoryParentUri: bool = Field(default=False, description="Include category parent URI.")
    includeLocationGeoLocation: bool = Field(default=False, description="Include geo location.")
    includeLocationPopulation: bool = Field(default=False, description="Include population size.")
    includeLocationGeoNamesId: bool = Field(default=False, description="Include GeoNames ID.")
    includeLocationCountryArea: bool = Field(default=False, description="Include country area.")
    includeLocationCountryContinent: bool = Field(default=False, description="Include continent.")

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
    url: str = Field(description="Article URL.")
    title: str = Field(description="Article title.")
    body: str = Field(description="Article body.")
    source: GlobalNewsSource = Field(description="Article source.")
    authors: list = Field(description="Article authors.")
    concepts: Optional[list[GlobalNewsConcept]] = Field(default=None, description="Article concepts.")
    image: Optional[str] = Field(default=None, description="Article image URL.")
    eventUri: Optional[str] = Field(default=None, description="Event URI.")
    shares: Optional[dict] = Field(default=None, description="Social media shares.")
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
